# -*- coding: utf-8 -*-
import typer
from jira.api.misc_client import MiscClient
import json

app = typer.Typer(help="Manage role")

@app.command(help="Get a role")
def get(
    project_id: str = typer.Argument(help="The project id"),
    role_id: str = typer.Argument(help="The role id")
    ):
    result = MiscClient().getRole(project_id, role_id)
    print(json.dumps(result, indent=2))
    return result
