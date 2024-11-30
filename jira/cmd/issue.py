# -*- coding: utf-8 -*-
import typer
from typing import Any
from jira.api.issue_client import IssueClient
import json

app = typer.Typer(help="Manage issues")

def get(issue_key: str = typer.Argument(help="The issue key"),
        fields: str = typer.Argument(help="The fields to select", default="*all")):
    result = IssueClient().getIssue(issue_key, fields)
    print(json.dumps(result, indent=2))
    return result

def delete_issue(issue_key: str = typer.Argument(help="The issue key")):
    result = IssueClient().deleteIssue(issue_key)
    print(json.dumps(result, indent=2))
    return result

def create_issue(json_file: str = typer.Argument(help="The JSON file containing the issue")):
    with open(json_file,'r') as issue_raw:
        issue = json.load(issue_raw)
        result = IssueClient().createIssue(issue)
        print(json.dumps(result, indent=2))
        return result

def update_issue(self):
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
            rc, current_issue_json = IssueClient().getIssue(issue_key)
            current_issue = json.loads(current_issue_json)
            issuetype_id = current_issue['fields']['issuetype']['id']
            project_key = current_issue['fields']['project']['id']
            rc, current_meta_json = IssueClient().getCreateMeta(project_key, issuetype_id)
            current_meta = json.loads(current_meta_json)
            targetFieldId = IssueClient().getFieldIdFromKeyAndMeta(field_key, current_meta)
            value = None
            if not(isLiteralValue):
                sourceFieldKey = value_or_field_key[1:]
                sourceFieldId = IssueClient().getFieldIdFromKeyAndMeta(sourceFieldKey, current_meta)
                value = current_issue['fields'][sourceFieldId]
            else:
                value = value_or_field_key
            # Now get the field id from the field name
            current_issue['fields'][targetFieldId] = value
            result = IssueClient().updateIssue(issue_key, field_key, value)
            print(json.dumps(result, indent=2))
            return result
            i = i + 1
    else:
        rc, current_issue_json = IssueClient().getIssue(issue_keys)
        current_issue = json.loads(current_issue_json)
        issuetype_id = current_issue['fields']['issuetype']['id']
        project_key = current_issue['fields']['project']['id']
        print('Get meta for ' + issue_keys + ', issuetype=' + str(issuetype_id) + ', project_key=' + str(project_key))
        rc, current_meta_json = IssueClient().getCreateMeta(project_key, issuetype_id)
        current_meta = json.loads(current_meta_json)
        targetFieldId = IssueClient().getFieldIdFromKeyAndMeta(field_key, current_meta)
        value = None
        if not(isLiteralValue):
            sourceFieldKey = value_or_field_key[1:]
            sourceFieldId = IssueClient().getFieldIdFromKeyAndMeta(sourceFieldKey, current_meta)
            value = current_issue['fields'][sourceFieldId]
        else:
            value = value_or_field_key
        # Now get the field id from the field name
        current_issue['fields'][targetFieldId] = value
        result = IssueClient().updateIssue(issue_keys, field_key, value)
        print(json.dumps(result, indent=2))
        return result

def get_create_meta(project_key: str = typer.Argument(help="The project key"),
               issue_key: str = typer.Argument(help="The issue key")):
    result = IssueClient().getCreateMeta(project_key, issue_key)
    print(json.dumps(result, indent=2))
    return result