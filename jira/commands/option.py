# -*- coding: utf-8 -*-
"""The session command."""

import sys

#reload(sys)
#sys.setdefaultencoding('utf8')

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Option(Base):
    """Manage options"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getOption()
        elif self.hasOption('add'):
            self.addOption()
        elif self.hasOption('del'):
            self.deleteOption()
        elif self.hasOption('replace'):
            self.replaceOption()
        elif self.hasOption('exist'):
            self.existOption()
        elif self.hasOption('getid'):
            self.getOptionId()
        elif self.hasOption('addcascading'):
            self.addCascadingOption()
        elif self.hasOption('delcascading'):
            self.delCascadingOption()
        else:
            print("Nothing to do.")

    # addcascading <field_key> <context_id> <parent_id> <option_value>
    def addCascadingOption(self):
        field_key = self.options['<field_key>']
        context_id = self.options['<context_id>']
        parent_id = self.options['<parent_id>']
        option_value = self.options['<option_value>']
        rc, datas = self.jira_client.addCascadingOption(field_key, context_id, parent_id, option_value)
        self.processResults(rc, datas)

    # delcascading <field_key> <context_id> <parent_id> <option_value>
    def delCascadingOption(self):
        field_key = self.options['<field_key>']
        context_id = self.options['<context_id>']
        parent_id = self.options['<parent_id>']
        option_id = self.options['<option_id>']
        rc, datas = self.jira_client.delCascadingOption(field_key, context_id, parent_id, option_id)
        self.processResults(rc, datas)

    def getOptionId(self):
        field_key = self.options['<field_key>']
        option_value = self.options['<option_value>']
        rc, datas = self.jira_client.getFieldOptions(field_key)
        option_values = json.loads(datas)['values']
        for current_option in option_values:
            current_option_value = current_option['value']
            if current_option_value == option_value:
                print(current_option['id'])
                break

    # replace <field_key> <option_to_replace> <option_to_use> <jql_filter>
    def replaceOption(self):
        field_key = self.options['<field_key>']
        option_to_replace = self.options['<option_to_replace>']
        option_to_use = self.options['<option_to_use>']
        jql_filter = self.options['<jql_filter>']
        rc, datas = self.jira_client.replaceOption(field_key, option_to_replace, option_to_use, jql_filter)
        print(datas)

    def existOption(self):
        field_key = self.options['<field_key>']
        option_value = self.options['<option_value>'].encode('utf-8')
        result = self.jira_client.hasOption(field_key, option_value)
        if result:
            print('TRUE')
        else:
            print('FALSE')

    def getOption(self):
        field_key = self.options['<field_key>']
        option_id = self.options['<option_id>']
        rc, datas = self.jira_client.getFieldOption(field_key, option_id)
        self.processResults(rc, datas)

    def deleteOption(self):
        field_key = self.options['<field_key>']
        option_id = self.options['<option_id>']
        if str(option_id).find('..') == -1:
            rc, datas = self.jira_client.deleteFieldOption(field_key, option_id)
            if rc != 204:
                try:
                    print(json.dumps(json.loads(datas), indent=2))
                except:
                    print(datas)
                self.processResults(rc, datas)
        else:
            options_limits = str(option_id).split('..')
            option_low = int(options_limits[0])
            option_high = int(options_limits[1])
            results = dict()
            for opt in range(option_low, option_high):
                rc, datas = self.jira_client.deleteFieldOption(field_key, opt)
                if rc != 204:
                    try:
                        errorMessages = json.loads(datas)['errorMessages']
                        if len(errorMessages) == 1:
                            results[opt] = errorMessages[0]
                        else:
                            results[opt] = errorMessages
                    except:
                        print(datas)
            print(json.dumps(results, indent=2))

    def addOption(self):
        field_key = self.options['<field_key>']
        option_value = self.options['<option_value>']
        project_keys = self.options['<project_keys>']
        projects = project_keys.split(',')
        config = dict(scope=dict(projects=projects))
        print("Will add %s option to field %s" % (option_value,field_key))
        if not self.jira_client.hasOption(field_key, option_value):
            jsonOption = dict(value=option_value, config=config)
            self.jira_client.addOption(field_key, jsonOption)

    def indexOf(self, item, array):
        idx = 0
        for i in array:
            if str(i) == str(item):
                return idx
            idx = idx+1
        return -1
