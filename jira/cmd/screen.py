# -*- coding: utf-8 -*-
import typer
from jira.api.screen_client import ScreenClient
import json

app = typer.Typer(help="Manage screens")

@app.command(help="Get a screen")
def getScreen(screen_id: str = typer.Argument(help="The screen id")):
    result = ScreenClient().getScreen(screen_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get tabs of a screen")
def getScreenTabs(
        screen_id: str = typer.Argument(help="The screen id"),
        project_id: str = typer.Argument(help="The project id")
        ):
    result = ScreenClient().getScreenTabs(screen_id, project_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Add a field to a screen tab")
def addFieldToTab(
        screen_id: str = typer.Argument(help="The screen id"),
        tab_id: str = typer.Argument(help="The tab id"),
        field_id: str = typer.Argument(help="The field id")
        ):
    result = ScreenClient().addFieldToTab(screen_id, tab_id, field_id)
    print(json.dumps(result, indent=2))
    return result
