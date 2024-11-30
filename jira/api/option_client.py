from jira.api.jira_client import JiraClient, indexOf
import httpx
import json
from typing import Any
import sys

class OptionClient(JiraClient):

  def hasOption(self, field_key: str, option_value: str) -> bool:
      options = self.getFieldOptions(field_key, "")
      allValues: list[str] = []
      for option in options:
          allValues.append(str(option['value'].encode('utf-8')))
      return indexOf(option_value, allValues) > -1

  def getFieldOption(self, field_key: str, option_id: str) -> Any:
    res = httpx.get(f"{self.server}/rest/api/3/field/{field_key}/option/{option_id}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def deleteFieldOption(self, field_key: str, option_id: str) -> Any:
    res = httpx.delete(f"{self.server}/rest/api/3/field/{field_key}/option/{option_id}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def addOptionWithId(self, field_key: str, option: dict[str,str], option_id: str) -> Any:
    res = httpx.put(f"{self.server}/rest/api/3/field/{field_key}/option/{option_id}", auth=self.auth, json=option)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def updateFieldOption(self, field_key: str, option: dict[str,str]) -> Any:
    res = httpx.put(f"{self.server}/rest/api/3/field/{field_key}/option/{option['id']}", auth=self.auth, json=option)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def replaceOption(self, field_key: str, option_to_replace: str, option_to_use: str, jql_filter: str) -> Any:
    params = {
      "replaceWith": option_to_use,
      "jql": jql_filter
    }
    res = httpx.delete(f"{self.server}/rest/api/3/field/{field_key}/option/{option_to_replace}/issue",
                        auth=self.auth,
                        params=params)
    if res.status_code == 303:
        print(f"Get task status here: {res.text}")
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getFieldOptions(self, field_key: str, context: str) -> list[dict[str,Any]]:
    if context:
      uri = f"{self.server}/rest/api/3/customFieldOption/{field_key}"
    else:
      uri = f"{self.server}/rest/api/3/field/{field_key}/context/{context}/option"
    isLast = False
    startAtIdx = 0
    maxResults = 1000
    error_code = 0
    error_message = ""
    all_options: list[dict[str,str]] = list()
    while not isLast:
      params = {
        "startAt": startAtIdx,
        "maxResults": maxResults
      }
      res = httpx.get(uri, params=params, auth=self.auth)
      if res.status_code == 200:
        payload = json.loads(res.text)
        all_options = all_options + payload['values']
        isLast = payload['isLast']
        if not isLast:
          startAtIdx = len(all_options)
      else:
        error_code = res.status_code
        error_message = res.text
        break
    if error_code == 0:
      return all_options
    print(f"Error {error_code}: {error_message}", file=sys.stderr)
    return list()

  def addOptionWithContext(self, field_key: str, context_id: str, option_value: str) -> Any:
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    payload = {
      "options": [
        {
          'disabled': False,
          'value': option_value
        }
      ]
    }
    res = httpx.post(f"{self.server}/rest/api/3/field/{field_key}/context/{context_id}/option", auth=self.auth, headers=headers, data=payload)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def delOptionWithContext(self, field_key: str, context_id: str, option_id: str) -> Any:
    res = httpx.delete(f"{self.server}/rest/api/3/field/{field_key}/context/{context_id}/option/{option_id}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def delAllOptionsWithContext(self, field_key: str, context_id: str) -> Any:
    options = self.getFieldOptions(field_key, context_id)
    results: list[Any] = list()
    for o in options:
      result = self.delOptionWithContext(field_key, context_id, o['id'])
      results.append(result)
    return results

  def addOption(self, field_key: str, option: str) -> Any:
    res = httpx.post(f"{self.server}/rest/api/3/field/{field_key}/option", auth=self.auth, json=option)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def addCascadingOption(self, field_key: str, contextId: str, parentOptionId: str, optionValue: str) -> Any:
    payload = {
      'options': [
        {
          'value': optionValue,
          'optionId': parentOptionId,
          'disabled': False
        }
      ]
    }
    res = httpx.post(f"{self.server}/rest/api/3/field/{field_key}/context/{contextId}/option", auth=self.auth, json=payload)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def delCascadingOption(self, field_key: str, contextId: str, parentOptionId: str, optionId: str):
    res = httpx.delete(f"{self.server}/rest/api/3/field/{field_key}/context/{contextId}/option/{optionId}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None
