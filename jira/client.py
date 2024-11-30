import typer

from jira.cmd import field
from jira.cmd import issuetype
from jira.cmd import option
from jira.cmd import page
from jira.cmd import project
from jira.cmd import role
from jira.cmd import screen
from jira.cmd import server
from jira.cmd import servicedesk
from jira.cmd import setting
from jira.cmd import task

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
app.add_typer(role.app, name="role")
app.add_typer(screen.app, name="screen")
app.add_typer(server.app, name="server")
app.add_typer(servicedesk.app, name="servicedesk")
app.add_typer(setting.app, name="setting")
app.add_typer(task.app, name="task")

if __name__ == '__main__':
    app()
