# -*- coding: utf-8 -*-
import typer
from typing import Any
from jira.api.field_client import FieldClient
from jira.api.option_client import OptionClient
from jira.api.issue_client import IssueClient
import yaml
import sys

EMPTY_DESCRIPTION: dict[str,Any] = {
                  "content": [
                    {
                      "content": [
                        {
                          "text": "Fluctuat nec mergitur",
                          "type": "text"
                        }
                      ],
                      "type": "paragraph"
                    }
                  ],
                  "type": "doc",
                  "version": 1
                }

app = typer.Typer(help="Sync fields", no_args_is_help=True)

@app.command(help="Check 2 custom fields between JIRA instances")
def check_fields(
    source_field: str = typer.Option(help="The source field key"),
    target_field: str = typer.Option(help="The target field key"),
    config: str = typer.Option(help="Config for sync")
    ):
    with open(config, 'r') as stream:
        try:
            config_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
        source_config: dict[str,str] = config_dict['source']
        target_config: dict[str,str] = config_dict['target']

        source_field_client = FieldClient(source_config)
        target_field_client = FieldClient(target_config)
        source_option_client = OptionClient(source_config)
        target_option_client = OptionClient(target_config)

        source_field_context = str(source_field_client.getFieldContexts(source_field)['values'][0]['id'])
        target_field_context = str(target_field_client.getFieldContexts(target_field)['values'][0]['id'])
        source_field_options = source_option_client.getFieldOptions(source_field, source_field_context)
        target_field_options = target_option_client.getFieldOptions(target_field, target_field_context)
        print(f"Got {len(source_field_options)} source options")
        print(f"Got {len(target_field_options)} target options")
        source_values = [x['value'] for x in source_field_options]
        target_values = [x['value'] for x in target_field_options]
        added_options_count = 0
        for source_option in source_values:
            if not source_option in target_values:
                print(f"Will add {source_option} to target")
                added_options_count += 1
        print(f"Would have added {added_options_count} options")
    return None

@app.command(help="Sync 2 custom fields between JIRA instances")
def sync_fields(
    source_field: str = typer.Option(help="The source field key"),
    target_field: str = typer.Option(help="The target field key"),
    config: str = typer.Option(help="Config for sync")
    ):
    with open(config, 'r') as stream:
        try:
            config_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
        source_config: dict[str,str] = config_dict['source']
        target_config: dict[str,str] = config_dict['target']

        source_field_client = FieldClient(source_config)
        target_field_client = FieldClient(target_config)
        source_option_client = OptionClient(source_config)
        target_option_client = OptionClient(target_config)

        source_field_context = str(source_field_client.getFieldContexts(source_field)['values'][0]['id'])
        target_field_context = str(target_field_client.getFieldContexts(target_field)['values'][0]['id'])
        source_field_options = source_option_client.getFieldOptions(source_field, source_field_context)
        target_field_options = target_option_client.getFieldOptions(target_field, target_field_context)
        print(f"Got {len(source_field_options)} source options")
        print(f"Got {len(target_field_options)} target options")
        source_values = [x['value'] for x in source_field_options]
        target_values = [x['value'] for x in target_field_options]
        added_options_count = 0
        options_to_create: list[dict[str, Any]] = list()
        for source_option in source_values:
            if not source_option in target_values:
                print(f"Adding {source_option} to target")
                options_to_create.append({
                    'value': source_option,
                    'disabled': False
                })
                added_options_count += 1
        if len(options_to_create) > 0:
            # iterate over the options_to_create by batch of 1000
            for i in range(0, len(options_to_create), 1000):
                batch = options_to_create[i:i+1000]
                target_option_client.addOptionsListWithContext(target_field, target_field_context, batch)

        print(f"Added {added_options_count} options")
    return None

@app.command(help="Check 2 boards between JIRA instances")
def check_issues(
    source_board: str = typer.Option(help="The source board"),
    target_board: str = typer.Option(help="The target board"),
    fields: str = typer.Option(help="The fields map"),
    config: str = typer.Option(help="Config for sync")
    ):
    with open(config, 'r') as stream:
        try:
            config_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
        source_config: dict[str,str] = config_dict['source']
        target_config: dict[str,str] = config_dict['target']

        source_issue_client = IssueClient(source_config)
        target_issue_client = IssueClient(target_config)

        source_fields = [y[0] for y in [x.split('=') for x in fields.split(',')]]
        target_fields = [y[1] for y in [x.split('=') for x in fields.split(',')]]
        fields_map = dict(zip(source_fields, target_fields))
        source_issues = source_issue_client.getIssues(f"project={source_board} order by created ASC", 100, ','.join(source_fields))
        target_issues = target_issue_client.getIssues(f"project={target_board} order by created ASC", 100, ','.join(target_fields))
        print(f"Got {len(source_issues)} source issues")
        print(f"Got {len(target_issues)} target issues")
        source_issues_map = {x['key']: x for x in source_issues}
        target_issues_map = {x['key']: x for x in target_issues}
        added_issues_count = 0
        updated_issues_count = 0
        for source_key in source_issues_map.keys():
            target_key = target_board + '-' + source_key.split('-')[1]
            if not target_key in target_issues_map: 
              print(f"Will add {target_key} for {source_key}")
              added_issues_count += 1
            elif issues_are_different(source_issues_map[source_key], target_issues_map[target_key], fields_map):
              print(f"Will update {target_key} for {source_key}")
              updated_issues_count += 1
        print(f"Would have added {added_issues_count} issues")
        print(f"Would have updated {updated_issues_count} issues")
    return None

@app.command(help="Sync 2 boards between JIRA instances")
def sync_issues(
    source_board: str = typer.Option(help="The source board"),
    target_board: str = typer.Option(help="The target board"),
    fields: str = typer.Option(help="The fields map"),
    config: str = typer.Option(help="Config for sync")
    ):
    with open(config, 'r') as stream:
        try:
            config_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
        source_config: dict[str,str] = config_dict['source']
        target_config: dict[str,str] = config_dict['target']

        source_issue_client = IssueClient(source_config)
        target_issue_client = IssueClient(target_config)

        source_fields = [y[0] for y in [x.split('=') for x in fields.split(',')]]
        target_fields = [y[1] for y in [x.split('=') for x in fields.split(',')]]
        fields_map = dict(zip(source_fields, target_fields))
        source_issues = source_issue_client.getIssues(f"project={source_board} order by created ASC", 100, ','.join(source_fields))
        target_issues = target_issue_client.getIssues(f"project={target_board} order by created ASC", 100, ','.join(target_fields))
        source_issues_map = {x['key']: x for x in source_issues}
        target_issues_map = {x['key']: x for x in target_issues}
        added_issues_count = 0
        added_issues: list[dict[str,Any]] = list()
        updated_issues_count = 0
        updated_issues: list[dict[str,Any]] = list()
        for source_key in source_issues_map.keys():
            target_key = target_board + '-' + source_key.split('-')[1]
            # Create new issue
            if not target_key in target_issues_map:
                source_issue = source_issues_map[source_key]
                target_issue = get_target_issue(source_issue, fields_map, target_board)
                added_issues.append(target_issue)
                added_issues_count += 1
            # Update issue
            elif issues_are_different(source_issues_map[source_key], target_issues_map[target_key], fields_map):
                source_issue = source_issues_map[source_key]
                target_issue = get_target_issue(source_issue, fields_map, target_board)
                target_issue['key'] = target_key
                updated_issues.append(target_issue)
                updated_issues_count += 1
        if len(added_issues) > 0:
            for i in range(0, len(added_issues), 50):
                batch = added_issues[i:i+50]
                update_issues = {
                    "issueUpdates": batch
                }
                print(f"[ADD] Batch {i+1}/{len(added_issues)/50}")
                result = target_issue_client.createIssues(update_issues)
                print(f"{result}")
        if len(updated_issues) > 0:
            updated_issues_count_done = 0
            for issue in updated_issues:
                issue_key: str = issue['key']
                del(issue['key'])
                print(f"[UPDATE] Issue {issue_key} ({updated_issues_count_done+1}/{len(updated_issues)})")
                print(f"{issue}")
                result = target_issue_client.updateIssueFull(issue_key, issue)
                print(f"{result}")
                updated_issues_count_done += 1
            print(f"Updated {updated_issues_count_done} issues")

    return None

def get_target_value(raw_value: Any) -> Any | None:
    if isinstance(raw_value, list):
        target_values: list[dict[str,str]] = []
        for v in raw_value:
            if 'value' in v:
                target_values.append({ 'value': v['value'] })
        return target_values
    elif raw_value is None:
        return None
    elif 'value' in raw_value:
        return { 'value': raw_value['value'] }
    return raw_value

def get_target_issue(source_issue: dict[str,Any], fields_map: dict[str,str], target_board: str) -> dict[str,Any]:
    source_issue_fields = source_issue['fields']
    target_issue_fields: dict[str,Any] = dict()
    for s in fields_map.keys():
        target_field = fields_map[s]
        raw_value = source_issue_fields[s]
        target_issue_fields[target_field] = get_target_value(raw_value)
    target_issue_fields['description'] = EMPTY_DESCRIPTION
    target_issue_fields['project'] = {
        'key': target_board
    }
    target_issue_fields['issuetype'] = {
        'name': 'Task'
    }
    target_issue: dict[str,Any] = {
        'fields': target_issue_fields,
        'update': {}
    }
    return target_issue

def issues_are_different(source_issue: dict[str,Any], target_issue: dict[str,Any], fields_map: dict[str,str] ) -> bool:
    source_fields = source_issue['fields']
    target_fields = target_issue['fields']
    for s in fields_map.keys():
        source_value = get_target_value(source_fields[s])
        target_value = get_target_value(target_fields[fields_map[s]])
        if source_value != target_value:
            return True
    return False
