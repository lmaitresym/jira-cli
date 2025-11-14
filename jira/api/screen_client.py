from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class ScreenClient(JiraClient):

  def getScreen(self, screen_id: str) -> dict[str, Any]:
    params = {
      'id': [ 
        int(screen_id)
      ]
    }
    res = httpx.get(f"{self.server}/rest/api/3/screens", auth=self.auth, params=params)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def getScreenTabs(self, screen_id: str, project_id: str) -> Any:
    params = {
      'projectKey': project_id
    }
    res = httpx.get(f"{self.server}/rest/api/2/screens/{screen_id}/tabs", auth=self.auth, params=params)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def addFieldToTab(self, screen_id: str, tab_id: str, field_id: str) -> Any:
    payload = {
      'fieldId': field_id
    }
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    res = httpx.post(f"{self.server}/rest/api/2/screens/{screen_id}/tabs/{tab_id}/fields", headers=headers, auth=self.auth, data=payload)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None
