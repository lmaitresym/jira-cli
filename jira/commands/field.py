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
        elif self.hasOption('getall'):
            self.getFields()
        elif self.hasOption('getbyid'):
            self.getFieldById()
        elif self.hasOption('getbyname'):
            self.getFieldByName()
        elif self.hasOption('delete'):
            self.deleteField()
        elif self.hasOption('trash'):
            self.trashField()
        elif self.hasOption('restore'):
            self.restoreField()
        elif self.hasOption('addoptions'):
            self.addOptions()
        elif self.hasOption('addoption'):
            self.addOption()
        elif self.hasOption('deloption'):
            self.delOption()
        elif self.hasOption('delalloptions'):
            self.delAllOptions()
        elif self.hasOption('suggestions'):
            self.suggestions()
        elif self.hasOption('referenceDatas'):
            self.referenceDatas()
        elif self.hasOption('getcontexts'):
            self.getContexts()
        elif self.hasOption('delcontext'):
            self.delContext()
        elif self.hasOption('create'):
            self.createField()
        else:
            print("Nothing to do.")

    def getField(self):
        field_key_or_id_or_name = self.options['<field_key_or_id_or_name>']
        rc, datas = self.jira_client.getFields()
        fields_list = json.loads(datas)
        results = list()
        for field in fields_list:
            if field['id'] == field_key_or_id_or_name or field['key'] == field_key_or_id_or_name or field['name'] == field_key_or_id_or_name:
                results.append(field)
        print(json.dumps(results, indent=2))

    def getFields(self):
        _, datas = self.jira_client.getFields()
        print(json.dumps(json.loads(datas), indent=2))

    def deleteField(self):
        field_id = self.options['<field_id>']
        rc, datas = self.jira_client.deleteField(field_id)
        self.processResults(rc, datas)

    def trashField(self):
        field_id = self.options['<field_id>']
        rc, datas = self.jira_client.trashField(field_id)
        self.processResults(rc, datas)

    def restoreField(self):
        field_id = self.options['<field_id>']
        rc, datas = self.jira_client.restoreField(field_id)
        self.processResults(rc, datas)

    def getFieldById(self):
        field_id = self.options['<custom_field_id>']
        rc, datas = self.jira_client.getCustomFieldById(field_id)
        if rc == 200:
            values = json.loads(datas)['values']
            if len(values) > 0:
                self.processResults(rc, json.dumps(json.loads(datas)['values'][0]))
            else:
                self.processResults(rc, "")
        else:
            self.processResults(rc, datas)

    def getFieldByName(self):
        field_name = self.options['<field_name>']
        rc, datas = self.jira_client.getFieldsByName(field_name)
        if rc == 200:
            self.processResults(rc, json.dumps(json.loads(datas)['values']))
        else:
            self.processResults(rc, datas)

    def createField(self):
        name = self.options['<name>']
        description = self.options['<description>']
        searcherKey = self.options['<searcher_key>']
        fieldType = self.options['<field_type>']
        rc, datas = self.jira_client.createCustomField( name, description, searcherKey, fieldType)
        self.processResults(rc, datas)

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
        context = self.options['<context>']
        rc, datas = self.jira_client.getFieldOptions(field_key, context)
        self.processResults(rc, datas)

    def getContexts(self):
        field_key = self.options['<field_key>']
        rc, datas = self.jira_client.getFieldContexts(field_key)
        self.processResults(rc, datas)

    def addProjectToOptions(self):
        field_key = self.options['<field_key>']
        project_id = self.options['<project_id>']
        rc, datas = self.jira_client.getFieldOptions(field_key)
        # print("Will add project " + project_id + " to options of " + field_key)
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

    def addOptions(self):
        field_key = self.options['<field_key>']
        options_file = self.options['<options_file>']
        project_keys = self.options['<project_keys>']
        option_values = []
        with open(options_file, 'r') as file:
            for line in file:
                line_clean = line.strip(' \t\n\r').encode('utf-8')
                #print line_clean
                option_values.append(line_clean)
        projects = project_keys.split(',')
        config = dict(scope=dict(projects=projects))
        print("Will add %d options to %s" % (len(option_values),field_key))
        results = []
        index = 1
        for option_value in option_values:
            print("Add option %d/%d" % (index,len(option_values)))
            if not self.jira_client.hasOption(field_key, option_value):
                jsonOption = dict(value=option_value, config=config)
                rc, datas = self.jira_client.addOption(field_key, jsonOption)
                results.append(datas)
            index += 1
        print(json.dumps(results))

    def addOption(self):
        field_key = self.options['<field_key>']
        option_value = self.options['<option_value>']
        context_id = self.options['<context_id>']
        rc, result = self.jira_client.addOptionWithContext(field_key, context_id, option_value)

    def delOption(self):
        field_key = self.options['<field_key>']
        option_id = self.options['<option_id>']
        context_id = self.options['<context_id>']
        rc, result = self.jira_client.delOptionWithContext(field_key, context_id, option_id)

    def delAllOptions(self):
        field_key = self.options['<field_key>']
        context_id = self.options['<context_id>']
        rc, result = self.jira_client.delAllOptionsWithContext(field_key, context_id)

    def suggestions(self):
        field_key = self.options['<field_key>']
        rc, datas = self.jira_client.getSuggestions(field_key)
        self.processResults(rc, datas)

    def referenceDatas(self):
        field_key = self.options['<field_key>']
        rc, datas = self.jira_client.getReferenceData(field_key)
        self.processResults(rc, datas)

    def delContext(self):
        field_id = self.options['<field_id>']
        context_id = self.options['<context_id>']
        rc, datas = self.jira_client.delContext(field_id, context_id)
        self.processResults(rc, datas)
