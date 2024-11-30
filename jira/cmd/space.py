# -*- coding: utf-8 -*-
import typer
from jira.api.page_client import PageClient
import json

app = typer.Typer(help="Manage spaces")

@app.command(help="Get a space")
def get(
    space_key: str = typer.Argument(help="The space key")
    ):
    result = PageClient().getSpace(space_key)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="List spaces")
def list():
    result = PageClient().getSpaces()
    print(json.dumps(result, indent=2))
    return result
