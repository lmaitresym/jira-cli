from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys
# import logging

# logging.basicConfig(
#     format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logging.DEBUG
# )

class ProjectClient(JiraClient):

  def getProject(self, project: str) -> Any:
    params = {
        "expand": [
            "description",
            "issueTypes",
            "lead",
            "projectKeys",
            "issueTypeHierarchy"
        ]
    }
    res = httpx.get(f"{self.server}/rest/api/3/project/{project}", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def listProjects(self) -> list[Any]:
    res = httpx.get(f"{self.server}/rest/api/3/project", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return []
