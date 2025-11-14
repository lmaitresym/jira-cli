# -*- coding: utf-8 -*-
import typer
from jira.api.issues_client import IssuesClient
import json

app = typer.Typer(help="Manage issues in bulk", no_args_is_help=True)

@app.command(help="Get bulk status of fields for issues")
def get_bulk_fields(issues_keys: str = typer.Argument(help="The issues keys, separated by comma")):
    result = IssuesClient().getBulkFields(issues_keys.split(','))
    print(json.dumps(result, indent=2))
    return result
