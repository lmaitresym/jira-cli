# -*- coding: utf-8 -*-
import typer
from jira.api.servicedesk_client import ServiceDeskClient
import json

app = typer.Typer(help="Manage service desks")

@app.command(help="Get a service desk")
def get(servicedesk_id: str = typer.Argument(help="The service desk id")):
    result = ServiceDeskClient().getServiceDesk(servicedesk_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="List service desks")
def listServiceDesks():
    result = ServiceDeskClient().listServiceDesks()
    print(json.dumps(result, indent=2))
    return result
