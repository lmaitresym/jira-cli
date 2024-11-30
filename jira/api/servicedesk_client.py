from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class ServiceClient(JiraClient):

  def getServiceDesk(self, servicedesk_id: str):
    res = httpx.get(f"{self.server}/rest/servicedeskapi/servicedesk/{servicedesk_id}", auth=self.auth)
    return r.status_code, r.content

  def listServiceDesks(self):
    res = httpx.get(f"{self.server}/rest/servicedeskapi/servicedesk", auth=self.auth)
    return r.status_code, r.content
