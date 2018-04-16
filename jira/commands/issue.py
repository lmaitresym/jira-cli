# -*- coding: utf-8 -*-
"""The issue command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Issue(Base):
    """Manage issues"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getIssue()
        elif self.hasOption('add'):
            self.addIssue()
        elif self.hasOption('del'):
            self.deleteIssue()
        elif self.hasOption('set'):
            self.updateIssue()
        elif self.hasOption('createmeta'):
            self.createMeta()
        else:
            print("Nothing to do.")

    def getIssue(self):
        issue_key = self.options['<issue_key>']
        rc, datas = self.jira_client.getIssue(issue_key)
        self.processResults(rc, datas)

    def deleteIssue(self):
        issue_key = self.options['<issue_key>']
        rc, datas = self.jira_client.deleteIssue(issue_key)
        if rc != 200:
            print(datas)
        self.processResults(rc, datas)

    def addIssue(self):
        pass

    def updateIssue(self):
        issue_keys = self.options['<issue_keys>']
        field_key = self.options['<field_key>']
        value_or_field_key = self.options['<value_or_field_key>']
        isLiteralValue = not(value_or_field_key.startswith('*'))
        if (str(issue_keys).find('..') > -1) or (str(issue_keys).find(',') > -1):
            # A key is like 'DSP-78'
            issue_keys_array = list()
            if str(issue_keys).find('..') > -1:
                issue_limits = str(issue_keys).split('..')
                project_key = str(issue_limits[0].split('-')[0])
                issue_low = int(issue_limits[0].split('-')[1])
                project_key2 = str(issue_limits[1].split('-')[0])
                if (project_key != project_key2):
                    raise ValueError('The issues must be on the same project (%s/%s).' % (project_key, project_key2))
                issue_high = int(issue_limits[1].split('-')[1])
                for id in range(issue_low, issue_high):
                    issue_keys_array.append(project_key + '-' + str(id))
            elif str(issue_keys).find(',') > -1:
                issue_keys_array = issue_keys.split(',')

            i = 1
            for issue_key in issue_keys_array:
                print("Update issue %s (%d/%d)" % (issue_key, i, len(issue_keys_array)))
                rc, current_issue_json = self.jira_client.getIssue(issue_key)
                current_issue = json.loads(current_issue_json)
                issuetype_id = current_issue['fields']['issuetype']['id']
                project_key = current_issue['fields']['project']['id']
                rc, current_meta_json = self.jira_client.getCreateMeta(project_key, issuetype_id)
                current_meta = json.loads(current_meta_json)
                targetFieldId = self.jira_client.getFieldIdFromKeyAndMeta(field_key, current_meta)
                value = None
                if not(isLiteralValue):
                    sourceFieldKey = value_or_field_key[1:]
                    sourceFieldId = self.jira_client.getFieldIdFromKeyAndMeta(sourceFieldKey, current_meta)
                    value = current_issue['fields'][sourceFieldId]
                else:
                    value = value_or_field_key
                # Now get the field id from the field name
                current_issue['fields'][targetFieldId] = value
                rc, datas = self.jira_client.updateIssue(issue_key, field_key, value)
                self.processResults(rc, datas)
                i = i + 1
        else:
            rc, current_issue_json = self.jira_client.getIssue(issue_keys)
            current_issue = json.loads(current_issue_json)
            issuetype_id = current_issue['fields']['issuetype']['id']
            project_key = current_issue['fields']['project']['id']
            print('Get meta for ' + issue_keys + ', issuetype=' + str(issuetype_id) + ', project_key=' + str(project_key))
            rc, current_meta_json = self.jira_client.getCreateMeta(project_key, issuetype_id)
            current_meta = json.loads(current_meta_json)
            targetFieldId = self.jira_client.getFieldIdFromKeyAndMeta(field_key, current_meta)
            value = None
            if not(isLiteralValue):
                sourceFieldKey = value_or_field_key[1:]
                sourceFieldId = self.jira_client.getFieldIdFromKeyAndMeta(sourceFieldKey, current_meta)
                value = current_issue['fields'][sourceFieldId]
            else:
                value = value_or_field_key
            # Now get the field id from the field name
            current_issue['fields'][targetFieldId] = value
            rc, datas = self.jira_client.updateIssue(issue_keys, field_key, value)
            self.processResults(rc, datas)

    def createMeta(self):
        project_key = self.options['<project_key>']
        issue_key = self.options['<issue_type>']
        rc, datas = self.jira_client.getCreateMeta(project_key, issue_key)
        print(datas)
