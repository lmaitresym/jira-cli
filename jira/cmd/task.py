# -*- coding: utf-8 -*-
import typer
from jira.api.misc_client import MiscClient
import json

app = typer.Typer(help="Manage tasks")

@app.command(help="Get a task")
def get(task_id: str = typer.Argument(help="The task id")):
    result = MiscClient().getTask(task_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Cancel a task")
def cancel(task_id: str = typer.Argument(help="The task id")):
    result = MiscClient().cancelTask(task_id)
    print(json.dumps(result, indent=2))
    return result