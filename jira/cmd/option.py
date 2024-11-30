# -*- coding: utf-8 -*-
import typer
from typing import Any
from jira.api.jira_client import indexOf
from jira.api.option_client import OptionClient
import json

app = typer.Typer(help="Manage options")

@app.command(help="Load options from a field to a field in some projects")
def load_options(field_key: str = typer.Argument(help="The field key"),
                options_file: str = typer.Argument(help="Options file"),
                project_ids: str = typer.Argument(help="Projects ids")
                ):
    projects = project_ids.split(',')
    config = dict(scope=dict(projects=projects))
    results: list[Any] = list()
    with open(options_file,'r') as options_raw:
        options = json.load(options_raw)
        for option_id in options:
            option_value = options[option_id]
            json_option = dict(id=option_id, value=option_value, config=config)
            results.append(OptionClient().addOptionWithId(field_key, json_option, option_id))
    print(json.dumps(results, indent=2))
    return results

@app.command(help="Get options of a field's context")
def get_options(field_key: str = typer.Argument(help="The field key"),
               context: str = typer.Argument(help="The context id")):
    options = OptionClient().getFieldOptions(field_key, context)
    print(json.dumps(options, indent=2))
    return options

@app.command(help="Add options to a project field")
def add_project_options(field_key: str = typer.Argument(help="The field key"),
                        project_id: str = typer.Argument(help="The project id")):
    options = OptionClient().getFieldOptions(field_key, project_id)
    # print("Will add project " + project_id + " to options of " + field_key)
    for option in options:
        if project_id not in option['config']['scope']['projects']:
            print("Need to patch " + json.dumps(option))
            option['config']['scope']['projects'].append(project_id)
            projects2_dict = dict(attributes=[],id=project_id)
            option['config']['scope']['projects2'].append(projects2_dict)
            OptionClient().updateFieldOption(field_key, option)

@app.command(help="Delete options of a project field")
def delete_project_options(field_key: str = typer.Argument(help="The field key"),
                        project_id: str = typer.Argument(help="The project id")):
    options = OptionClient().getFieldOptions(field_key, project_id)
    print("Will remove project " + project_id + " to options of " + field_key)
    print("Got " + str(len(options)) + " options")
    for option in options:
        objarray = option['config']['scope']['projects']
        idx = indexOf(project_id, objarray)
        if idx > -1:
            print("OK")
            if len(option['config']['scope']['projects']) == 1:
                print("Need to delete option " + str(option['id']))
                OptionClient().deleteFieldOption(field_key, option['id'])
        else:
            print("KO, no ref to " + str(project_id) + " in " + json.dumps(option))

@app.command(help="Add several options from a file to a field's context")
def add_options(field_key: str = typer.Argument(help="The field key"),
                options_file: str = typer.Argument(help="The option file"),
                project_keys: str = typer.Argument(help="The project keys")
    ):
    option_values: list[str] = list()
    with open(options_file, 'r') as file:
        for line in file:
            line_clean = str(line.strip(' \t\n\r').encode('utf-8'))
            #print line_clean
            option_values.append(line_clean)
    projects = project_keys.split(',')
    config = dict(scope=dict(projects=projects))
    print("Will add %d options to %s" % (len(option_values),field_key))
    results: list[Any] = []
    index = 1
    for option_value in option_values:
        print("Add option %d/%d" % (index,len(option_values)))
        if not OptionClient().hasOption(field_key, option_value):
            jsonOption = dict(value=option_value, config=config)
            result = OptionClient().addOption(field_key, json.dumps(jsonOption))
            results.append(result)
        index += 1
    print(json.dumps(results))

@app.command(help="Add an option to a field's context")
def add_option(field_key: str = typer.Argument(help="The field key"),
                option_value: str = typer.Argument(help="The option value"),
                context_id: str = typer.Argument(help="The context id")
    ):
    result = OptionClient().addOptionWithContext(field_key, context_id, option_value)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Delete an option from a field's context")
def delete_option(
            field_key: str = typer.Argument(help="The field key"),
            option_id: str = typer.Argument(help="The option id"),
            context_id: str = typer.Argument(help="The context id")
              ):
    result = OptionClient().delOptionWithContext(field_key, context_id, option_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Delete all options of a field's context")
def delete_all_options(
        field_key: str = typer.Argument(help="The field key"),
        context_id: str = typer.Argument(help="The context id")
    ):
    result = OptionClient().delAllOptionsWithContext(field_key, context_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Add a cascading option")
def add_cascading(
            field_key: str = typer.Argument(help="The field key"),
            context_id: str = typer.Argument(help="The context id"),
            parent_id: str = typer.Argument(help="The parent id"),
            option_value: str = typer.Argument(help="The option value")
    ):
    result = OptionClient().addCascadingOption(field_key, context_id, parent_id, option_value)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Delete a cascading option")
def delete_cascading(
        field_key: str = typer.Argument(help="The field key"),
        context_id: str = typer.Argument(help="The context id"),
        parent_id: str = typer.Argument(help="The parent id"),
        option_id: str = typer.Argument(help="The option id")
        ):
    result = OptionClient().delCascadingOption(field_key, context_id, parent_id, option_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get the id of an option")
def get_id(
        field_key: str = typer.Argument(help="The field key"),
        option_value: str = typer.Argument(help="")
        ):
    options = OptionClient().getFieldOptions(field_key, "")
    for current_option in options:
        current_option_value = current_option['value']
        if current_option_value == option_value:
            print(current_option['id'])
            break

@app.command(help="Replace an option")
def replace(
        field_key: str = typer.Argument(help="The field key"),
        option_to_replace: str = typer.Argument(help=""),
        option_to_use: str = typer.Argument(help=""),
        jql_filter: str = typer.Argument(help="")
        ):
    result = OptionClient().replaceOption(field_key, option_to_replace, option_to_use, jql_filter)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get an option")
def get(
        field_key: str = typer.Argument(help="The field key"),
        option_id: str = typer.Argument(help="")
        ):
    result = OptionClient().getFieldOption(field_key, option_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Delete an option")
def delete(field_key: str = typer.Argument(help="The field key"),
    option_id: str = typer.Argument(help="")):
    if str(option_id).find('..') == -1:
        result = OptionClient().deleteFieldOption(field_key, option_id)
        print(json.dumps(result, indent=2))
        return result
    else:
        options_limits = str(option_id).split('..')
        option_low = int(options_limits[0])
        option_high = int(options_limits[1])
        results: list[Any] = list()
        for opt in range(option_low, option_high):
            result = OptionClient().deleteFieldOption(field_key, str(opt))
            results.append(result)
        print(json.dumps(results, indent=2))
        return results

@app.command(help="Add an option to one or more projects")
def add(
        field_key: str = typer.Argument(help="The field key"),
        option_value: str = typer.Argument(help="The option value"),
        project_keys: str = typer.Argument(help="The project keys")
    ):
    projects = project_keys.split(',')
    config = dict(scope=dict(projects=projects))
    print("Will add %s option to field %s" % (option_value,field_key))
    if not OptionClient().hasOption(field_key, option_value):
        jsonOption = dict(value=option_value, config=config)
        OptionClient().addOption(field_key, json.dumps(jsonOption))
