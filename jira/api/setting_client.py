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
    return r.status_code, r.content

  def getSetting(self, setting_key: str) -> Any:
    params = {
      "key": setting_key
    }
    res = httpx.get(f"{self.server}/rest/api/3/application-properties", params=params, auth=self.auth)
    return r.status_code, r.content

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
    return r.status_code, r.content
