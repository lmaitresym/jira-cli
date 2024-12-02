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

  def __init__(self):
    self.server: str = jira_config["server"]
    self.auth: tuple[str,str] = (jira_config["user"], jira_config["token"])
    self.headers = {
      "Accept": "application/json"
    }

