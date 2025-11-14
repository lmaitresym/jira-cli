from typing import Any

jira_config: dict[str,str] = {} 

def configure_jira_client(server: str, user: str, token: str):
    jira_config["server"] = server
    jira_config["user"] = user
    jira_config["token"] = token

def indexOf(item: Any, array: list[Any]) -> int:
    idx = 0
    for i in array:
        if str(i) == str(item):
            return idx
        idx = idx+1
    return -1

class JiraClient(object):

  server: str
  auth: tuple[str,str]

  def __init__(self, custom_jira_config: dict[str,str] | None = None):
    config: dict[str,str] = custom_jira_config if custom_jira_config is not None else jira_config
    self.server: str = config["server"]
    self.auth: tuple[str,str] = (config["user"], config["token"])
    self.headers = {
      "Accept": "application/json"
    }
