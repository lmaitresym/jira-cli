# -*- coding: utf-8 -*-
import typer
from typing import Any
from jira.api.issue_client import IssueClient
from jira.api.field_client import FieldClient
import json

app = typer.Typer(help="Manage issues")

@app.command(help="Get an issue")
def get(
    issue_key: str = typer.Argument(help="The issue key"),
    fields: str = typer.Argument(help="The fields to select", default="*all")
    ):
    result = IssueClient().getIssue(issue_key, fields)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Delete an issue")
def delete(
    issue_key: str = typer.Argument(help="The issue key")
    ):
    result = IssueClient().deleteIssue(issue_key)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Create an issue")
def create(
    json_file: str = typer.Argument(help="The JSON file containing the issue")
    ):
    with open(json_file,'r') as issue_raw:
        issue = json.load(issue_raw)
        result = IssueClient().createIssue(issue)
        print(json.dumps(result, indent=2))
        return result

@app.command(help="Update an issue")
def update_issue(
        issue_keys: str = typer.Argument(help="The issue keys"),
        field_key: str = typer.Argument(help="The field key"),
        value_or_field_key: str = typer.Argument(help="The value or field key")
        ):
    isLiteralValue = not(value_or_field_key.startswith('*'))
    if (str(issue_keys).find('..') > -1) or (str(issue_keys).find(',') > -1):
        # A key is like 'DSP-78'
        issue_keys_array: list[str] = list()
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
            current_issue: dict[str, Any] = IssueClient().getIssue(issue_key, None)
            issuetype_id = current_issue['fields']['issuetype']['id']
            project_key = current_issue['fields']['project']['id']
            current_meta = IssueClient().getCreateMeta(project_key, issuetype_id)
            targetFieldId = FieldClient().getFieldIdFromKeyAndMeta(field_key, current_meta)
            value = None
            if not(isLiteralValue):
                sourceFieldKey = value_or_field_key[1:]
                sourceFieldId = FieldClient().getFieldIdFromKeyAndMeta(sourceFieldKey, current_meta)
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
        current_issue: dict[str, Any] = IssueClient().getIssue(issue_keys)
        issuetype_id = current_issue['fields']['issuetype']['id']
        project_key = current_issue['fields']['project']['id']
        print('Get meta for ' + issue_keys + ', issuetype=' + str(issuetype_id) + ', project_key=' + str(project_key))
        rc, current_meta_json = IssueClient().getCreateMeta(project_key, issuetype_id)
        current_meta = json.loads(current_meta_json)
        targetFieldId = FieldClient().getFieldIdFromKeyAndMeta(field_key, current_meta)
        value = None
        if not(isLiteralValue):
            sourceFieldKey = value_or_field_key[1:]
            sourceFieldId = FieldClient().getFieldIdFromKeyAndMeta(sourceFieldKey, current_meta)
            value = current_issue['fields'][sourceFieldId]
        else:
            value = value_or_field_key
        # Now get the field id from the field name
        current_issue['fields'][targetFieldId] = value
        result = IssueClient().updateIssue(issue_keys, field_key, value)
        print(json.dumps(result, indent=2))
        return result

@app.command(help="Get the metadatas to create an issue")
def get_create_meta(project_key: str = typer.Argument(help="The project key"),
               issue_key: str = typer.Argument(help="The issue key")):
    result = IssueClient().getCreateMeta(project_key, issue_key)
    print(json.dumps(result, indent=2))

@app.command(help="Get isssues")
def getIssues(
        jql: str = typer.Argument(help="The JQL query to get the issues"),
        page_index: int = typer.Argument(help="The page to fetch"),
        page_size: int = typer.Argument(help="The page size", default=100),
        fields: str = typer.Argument(help="The fields to select", default="*all")
    ):
    by_page = False
    if page_index:
        by_page = True
    if by_page:
        #print("Get page %s/%s of issues for jql %s" % (page_index, page_size, jql))
        result = IssueClient().getIssuesPage(jql, page_index, page_size, fields.split(","))
    else:
        result = IssueClient().getIssues(jql, page_size, fields)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get the keys of issues matching a JQL query")
def getIssuesKeys(jql: str = typer.Argument(help="The issues keys to query")) -> list[str]:
    issues = IssueClient().getIssues(jql, None, None)
    issuesKeys: list[str] = list()
    for issue in issues:
        issuesKeys.append(issue['key'])
    print(json.dumps(issuesKeys, indent=2))
    return issuesKeys

@app.command(help="Create issues from a JSON file")
def createIssues(json_file: str = typer.Argument(help="A JSON file containing the issues to create")):
    with open(json_file,'r') as issues_raw:
        issues = json.load(issues_raw)
        results = IssueClient().createIssues(issues)
        print(json.dumps(results, indent=2))
        return results

