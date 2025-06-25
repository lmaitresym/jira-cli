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

@app.command(help="Sync 2 custom cascading fields between JIRA instances")
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

@app.command(help="Sync 2 custom fields between JIRA instances")
def sync_cascading_fields(
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
        target_values = [x['value'] for x in target_field_options]
        parent_to_children_map: dict[str,list[str]] = dict()
        children_to_parent_map: dict[str,str] = dict()
        source_options_map: dict[str,Any] = {x['id']:x for x in source_field_options}
        parent_options: dict[str,Any] = {}
        child_options: dict[str,Any] = {}
        for source_option in source_field_options:
            source_value = source_option['value']
            if 'optionId' in source_option:
                child_options[source_value] = {
                    'value': source_value,
                    'disabled': False
                }
                parent_id = source_option['optionId']
                parent_value = source_options_map[parent_id]['value']
                if not parent_value in parent_to_children_map.keys():
                    parent_to_children_map[parent_value] = list()
                parent_to_children_map[parent_value].append(source_value)
                children_to_parent_map[source_value] = parent_value
            else:
                parent_options[source_value] = {
                    'value': source_value,
                    'disabled': False
                }
        added_options_count = 0
        # We create parent options
        options_to_create: list[dict[str, Any]] = list()
        for source_value in parent_options.keys():
            if not source_value in target_values:
                print(f"Adding {source_value} to target")
                options_to_create.append(parent_options[source_value])
                added_options_count += 1
        created_parent_options: list[dict[str,Any]] = list()
        if len(options_to_create) > 0:
            # iterate over the options_to_create by batch of 1000
            for i in range(0, len(options_to_create), 1000):
                batch = options_to_create[i:i+1000]
                created_parent_options.extend(target_option_client.addOptionsListWithContext(target_field, target_field_context, batch)['options'])
        print(f"Added {added_options_count} parent options")
        print(f"Loaded back {len(created_parent_options)} new parent options")
        created_parent_options_map: dict[str,Any] = {x['value']:x['id'] for x in created_parent_options}
        # We create child options
        options_to_create: list[dict[str, Any]] = list()
        added_options_count = 0
        for source_value in child_options.keys():
            if not source_value in target_values:
                print(f"Adding {source_value} to target")
                parent_value = children_to_parent_map[source_value]
                child_value = child_options[source_value]
                child_value['optionId'] = created_parent_options_map[parent_value]
                options_to_create.append(child_options[source_value])
                added_options_count += 1
        created_child_options: list[dict[str,Any]] = list()
        if len(options_to_create) > 0:
            # iterate over the options_to_create by batch of 1000
            for i in range(0, len(options_to_create), 1000):
                batch = options_to_create[i:i+1000]
                created_child_options.extend(target_option_client.addOptionsListWithContext(target_field, target_field_context, batch)['options'])
        print(f"Added {added_options_count} child options")
        print(f"Loaded back {len(created_child_options)} new child options")
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
        # To test: project=SIE and id >= SIE-10164 order by created DESC
        # source_issues = source_issue_client.getIssues(f"project={source_board} and id >={source_board}-9000 order by created ASC", 100, ','.join(source_fields))
        # target_issues = target_issue_client.getIssues(f"project={target_board} and id >={target_board}-9000 order by created ASC", 100, ','.join(target_fields))
        source_issues = source_issue_client.getIssues(f"project={source_board} order by created ASC", 100, ','.join(source_fields))
        target_issues = target_issue_client.getIssues(f"project={target_board} order by created ASC", 100, ','.join(target_fields))
        print(f"Got {len(source_issues)} source issues")
        print(f"Got {len(target_issues)} target issues")
        source_issues_map = {x['key']: x for x in source_issues}
        target_issues_map = {x['key']: x for x in target_issues}
        added_issues: list[dict[str,Any]] = list()
        updated_issues: list[dict[str,Any]] = list()
        deleted_issues_count = 0
        deleted_issues: list[str] = list()
        # Delete issues
        for target_key in target_issues_map.keys():
            source_key = source_board + '-' + target_key.split('-')[1]
            if not source_key in source_issues_map.keys():
                print(f"Delete {target_key}/{source_key}")
                deleted_issues.append(target_key)
        for source_key in source_issues_map.keys():
            target_key = target_board + '-' + source_key.split('-')[1]
            # Create new issue
            if not target_key in target_issues_map.keys():
                print(f"Add {source_key}/{target_key}/{target_issues_map.keys()}")
                source_issue = source_issues_map[source_key]
                target_issue = get_target_issue(source_issue, fields_map, target_board)
                added_issues.append(target_issue)
            # Update issue
            elif issues_are_different(source_issues_map[source_key], target_issues_map[target_key], fields_map):
                print(f"Update {source_key}/{target_key}")
                source_issue = source_issues_map[source_key]
                target_issue = get_target_issue(source_issue, fields_map, target_board)
                target_issue['key'] = target_key
                updated_issues.append(target_issue)
        if len(added_issues) > 0:
            for i in range(0, len(added_issues), 50):
                batch = added_issues[i:i+50]
                update_issues = {
                    "issueUpdates": batch
                }
                print(f"[ADD] Batch {int((i)/50)+1}/{int(len(added_issues)/50)+1}")
                result = target_issue_client.createIssues(update_issues)
                print(f"{result}")
            print(f"Added {len(added_issues)} issues")
        if len(updated_issues) > 0:
            updated_issues_count_done = 0
            for issue in updated_issues:
                issue_key: str = issue['key']
                del(issue['key'])
                print(f"[UPDATE] Issue {issue_key} ({updated_issues_count_done+1}/{len(updated_issues)})")
                print(f"{issue}")
                result = target_issue_client.updateIssueFull(issue_key, issue)
                # print(f"{result}")
                updated_issues_count_done += 1
            print(f"Updated {updated_issues_count_done} issues")
        if len(deleted_issues) > 0:
            print(f"Will delete {len(deleted_issues)} issues")
            for issue_key in deleted_issues:
                target_issue_client.deleteIssue(issue_key)
                deleted_issues_count += 1
            print(f"Deleted {deleted_issues_count} issues")

    return None

def get_target_value(raw_value: Any) -> Any | None:
    if raw_value is None:
        return None
    elif isinstance(raw_value, list):
        target_values: list[Any] = []
        for v in raw_value:
            target_values.append(get_target_value(v))
        return target_values
    elif isinstance(raw_value, dict) and 'value' in raw_value:
        target_value: dict[str,Any] = { 'value': raw_value['value'] }
        if 'child' in raw_value:
            target_value['child'] = get_target_value(raw_value['child'])
        return target_value
    return raw_value

def get_target_issue(source_issue: dict[str,Any], fields_map: dict[str,str], target_board: str) -> dict[str,Any]:
    source_issue_fields = source_issue['fields']
    target_issue_fields: dict[str,Any] = dict()
    for source_field in fields_map.keys():
        target_field = fields_map[source_field]
        source_value = source_issue_fields[source_field]
        target_issue_fields[target_field] = get_target_value(source_value)
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
