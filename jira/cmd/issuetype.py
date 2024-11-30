# -*- coding: utf-8 -*-
import typer
from jira.api.issuetype_client import IssueTypeClient
import json

app = typer.Typer(help="Manage issue types")

@app.command(help="Get an issue type")
def get(issuetype_key: str = typer.Argument(help="Issue type key")):
    result = IssueTypeClient().getIssueType(issuetype_key)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get all issue types")
def get_all():
    result = IssueTypeClient().getIssueTypes()
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Get all issue types of a project")
def get_all_by_project(project_id: str = typer.Argument(help="The project id")):
    result = IssueTypeClient().getIssueTypesByProject(project_id)
    print(json.dumps(result, indent=2))
    return result

# @app.command(help="Delete an issue type")
# def delete(issuetype_id: str = typer.Argument(help="The issue type id")):
#     result = IssueTypeClient().deleteIssueType(issuetype_id)
#     print(json.dumps(result, indent=2))
#     return result

# @app.command(help="Create an issue type")
# def create(issuetype_name: str = typer.Argument(help="The issue type name"),
#             issuetype_description: str = typer.Argument(help="The issue type description"),
#             issuetype_hierarchy_level: str = typer.Argument(help="The issue type hierarchy level")
#     ):
#     result = IssueTypeClient().createIssueType(issuetype_name, issuetype_description, issuetype_hierarchy_level)
#     print(json.dumps(result, indent=2))
#     return result
