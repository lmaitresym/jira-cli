# -*- coding: utf-8 -*-
"""The project command."""
import typer
import json
from jira.api.project_client import ProjectClient

app = typer.Typer(help="Manage projects")

# ❯ poetry run jira-cli project get --project ESI
@app.command(help="Get project")
def get(
                    project: str = typer.Argument(help="The project key or id")
                ):
    project_client = ProjectClient()
    project = project_client.getProject(project)
    print(f"{json.dumps(project)}")
    return project

# ❯ poetry run jira-cli project list-projects
@app.command(help="List projects")
def list():
    project_client = ProjectClient()
    projects = project_client.listProjects()
    print(f"{json.dumps(projects)}")
    return projects
