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
        else:
            print("Nothing to do.")

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