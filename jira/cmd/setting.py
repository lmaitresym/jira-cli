# -*- coding: utf-8 -*-
import typer
from jira.api.setting_client import SettingClient
import json

app = typer.Typer(help="Manage settings")

@app.command(help="Get a setting")
def get(setting_key : str = typer.Argument(help="The setting key")):
    result = SettingClient().getSetting(setting_key)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Set a setting")
def set(
        setting_key: str = typer.Argument(help="The setting key"),
        setting_value: str = typer.Argument(help="The setting value")
    ):
    result = SettingClient().setSetting(setting_key, setting_value)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="List settings")
def list(category: str = typer.Argument(help="The category of settings", default=None)):
    result = SettingClient().listSettings(category)
    print(json.dumps(result, indent=2))
    return result
