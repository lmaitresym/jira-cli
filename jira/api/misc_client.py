from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class MiscClient(JiraClient):

  def getRole(self, project_id: str, role_id: str) -> dict[str,Any]:
    res = httpx.get(f"{self.server}/rest/api/3/project/{project_id}/role/{role_id}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def getTask(self, task_id: str) -> dict[str,Any]:
    res = httpx.get(f"{self.server}/rest/api/3/task/{task_id}", headers=self.headers, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def cancelTask(self, task_id: str) -> Any:
    res = httpx.get(f"{self.server}/rest/api/3/task/{task_id}/cancel", headers=self.headers, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getServerInfos(self) -> dict[str,Any]:
    res = httpx.get(f"{self.server}/rest/api/3/serverInfo", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}
