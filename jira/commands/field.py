# -*- coding: utf-8 -*-
"""The session command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Field(Base):
    """Manage fields"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('getoptions'):
            self.getOptions()
        elif self.hasOption('addprojectoptions'):
            self.addProjectToOptions()
        elif self.hasOption('delprojectoptions'):
            self.delProjectToOptions()
        elif self.hasOption('loadoptions'):
            self.loadOptions()
        elif self.hasOption('get'):
            self.getField()
        else:
            print("Nothing to do.")

    def getField(self):
        field_key_or_id_or_name = self.options['<field_key_or_id_or_name>']
        rc, datas = self.jira_client.getFields()
        fields_list = json.loads(datas)
        for field in fields_list:
            if field['id'] == field_key_or_id_or_name or field['key'] == field_key_or_id_or_name or field['name'] == field_key_or_id_or_name:
                print json.dumps(field)
                break

    def loadOptions(self):
        field_key = self.options['<field_key>']
        options_file = self.options['<options_file>']
        project_ids = self.options['<project_ids>']
        projects = project_ids.split(',')
        config = dict(scope=dict(projects=projects))
        with open(options_file,'r') as options_raw:
            options = json.load(options_raw)
            for option_id in options:
                option_value = options[option_id]
                json_option = dict(id=option_id, value=option_value, config=config)
                self.jira_client.addOptionWithId(field_key, json_option, option_id)

    def getOptions(self):
        field_key = self.options['<field_key>']
        rc, datas = self.jira_client.getFieldOptions(field_key)
        self.processResults(rc, datas)

    def addProjectToOptions(self):
        field_key = self.options['<field_key>']
        project_id = self.options['<project_id>']
        rc, datas = self.jira_client.getFieldOptions(field_key)
        print("Will add project " + project_id + " to options of " + field_key)
        options = json.loads(datas)['values']
        for option in options:
            if project_id not in option['config']['scope']['projects']:
                print("Need to patch " + json.dumps(option))
                option['config']['scope']['projects'].append(project_id)
                projects2_dict = dict(attributes=list(),id=project_id)
                option['config']['scope']['projects2'].append(projects2_dict)
                self.jira_client.updateFieldOption(field_key, option)

    def delProjectToOptions(self):
        field_key = self.options['<field_key>']
        project_id = self.options['<project_id>']
        rc, datas = self.jira_client.getFieldOptions(field_key)
        print("Will remove project " + project_id + " to options of " + field_key)
        options = json.loads(datas)['values']
        print("Got " + str(len(options)) + " options")
        for option in options:
            objarray = option['config']['scope']['projects']
            idx = self.indexOf(project_id, objarray)
            if idx > -1:
                print("OK")
                if len(option['config']['scope']['projects']) == 1:
                    print("Need to delete option " + str(option['id']))
                    self.jira_client.deleteFieldOption(field_key, option)
            else:
                print("KO, no ref to " + str(project_id) + " in " + json.dumps(option))

    def indexOf(self, item, array):
        idx = 0
        for i in array:
            print("i/item" + str(i) + '/' + str(item))
            if str(i) == str(item):
                return idx
            idx = idx+1
        return -1