from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class SettingClient(JiraClient):

  def listSettings(self, category: str) -> list[Any]:
    url: str
    if category == 'global':
      url = f"{self.server}/rest/api/3/configuration"
    elif category == 'advanced':
      url = f"{self.server}/rest/api/3/application-properties/advanced-settings"
    else:
      url = f"{self.server}/rest/api/3/application-properties"
    res = httpx.get(url, auth=self.auth)    
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return []

  def getSetting(self, setting_key: str) -> Any:
    params = {
      "key": setting_key
    }
    res = httpx.get(f"{self.server}/rest/api/3/application-properties", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def setSetting(self, setting_key: str, setting_value: str) -> Any:
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    payload = {
      "id": setting_key,
      "value": setting_value
    }
    res = httpx.put(f"{self.server}/rest/api/3/application-properties/{setting_key}", data=payload, headers=headers, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None
