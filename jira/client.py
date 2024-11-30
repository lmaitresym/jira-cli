import typer

from jira.cmd import field
from jira.cmd import issuetype
from jira.cmd import option
from jira.cmd import page
from jira.cmd import project
from jira.api.jira_client import jira_config

def init_config(
    server: str = typer.Option(help="The server to use", envvar="JIRA_SERVER"),
    user: str = typer.Option(help="The user", envvar="JIRA_USER"),
    token: str = typer.Option(help="The password/API token", envvar="JIRA_PASSWORD")
    ):
  jira_config["server"] = server
  jira_config["user"] = user
  jira_config["token"] = token

app = typer.Typer(callback=init_config)
app.add_typer(field.app, name="field")
app.add_typer(issuetype.app, name="issuetype")
app.add_typer(option.app, name="option")
app.add_typer(page.app, name="page")
app.add_typer(project.app, name="project")

if __name__ == '__main__':
    app()
