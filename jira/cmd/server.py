# -*- coding: utf-8 -*-
import typer
from jira.api.misc_client import MiscClient
import json

app = typer.Typer(help="Manage server")

@app.command(help="Get server infos")
def infos():
    result = MiscClient().getServerInfos()
    print(json.dumps(result, indent=2))
    return result
