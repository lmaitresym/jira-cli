from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class ServiceDeskClient(JiraClient):

  def getServiceDesk(self, servicedesk_id: str) -> dict[str, Any]:
    res = httpx.get(f"{self.server}/rest/servicedeskapi/servicedesk/{servicedesk_id}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def listServiceDesks(self) -> list[dict[str,Any]]:
    res = httpx.get(f"{self.server}/rest/servicedeskapi/servicedesk", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return []
