# -*- coding: utf-8 -*-
import typer
from typing import Any
from jira.api.jira_client import indexOf
from jira.api.field_client import FieldClient
import json

app = typer.Typer(help="Manage fields")

@app.command(help="Get a Field")
def get(
    field: str = typer.Argument(help="The field key or id")
    ):
    fields_list = FieldClient().getFields()
    results: list[dict[str, Any]] = list()
    for f in fields_list:
        if f['id'] == field or f['key'] == field or f['name'] == field:
            results.append(f)
    print(json.dumps(results, indent=2))
    return results

@app.command(help="Get all fields")
def get_fields():
    fields_list = FieldClient().getFields()
    print(json.dumps(fields_list, indent=2))
    return fields_list

@app.command(help="Delete a field, it must already be in the trash")
def delete_field(field_id: str = typer.Argument(help="The field id")):
    result = FieldClient().deleteField(field_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Put a field to the trash")
def trash_field(
    field_id: str = typer.Argument(help="The field id")
    ):
    result = FieldClient().trashField(field_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Restore a field from the trash")
def restore_field(field_id: str = typer.Argument(help="The field id")):
    result = FieldClient().restoreField(field_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get a field by ID")
def get_field_by_id(field_id: str = typer.Argument(help="The field id")):
    result = FieldClient().getCustomFieldById(field_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get a field by its name")
def get_field_by_name(field_name: str = typer.Argument(help="The field name")):
    result = FieldClient().getFieldsByName(field_name)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Create a field")
def create_field(field_name: str = typer.Argument(help="The field name"),
                description: str = typer.Argument(help="The description"),
                searcherKey: str = typer.Argument(help="The searcher key"),
                fieldType: str = typer.Argument(help="The field type")
    ):
    result = FieldClient().createCustomField( field_name, description, searcherKey, fieldType)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get contexts of a field")
def get_contexts(field_key: str = typer.Argument(help="The field key")):
    result = FieldClient().getFieldContexts(field_key)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Delete a context of a field")
def delete_context(field_id: str = typer.Argument(help="The field id"),
               context_id: str = typer.Argument(help="The context id")):
    result = FieldClient().deleteCustomFieldContext(field_id, context_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get suggestions for a field")
def suggestions(field_key: str = typer.Argument(help="The field key")):
    result = FieldClient().getSuggestions(field_key)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get reference data of a field")
def reference_datas(field_key: str = typer.Argument(help="The field key")):
    result = FieldClient().getReferenceData(field_key)
    print(json.dumps(result, indent=2))
    return result

