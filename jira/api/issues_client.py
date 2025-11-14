from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class IssuesClient(JiraClient):

  def deleteIssues(self, issues_keys: list[str]) -> dict[str,Any]:
    payload = {
      "selectedIssueIdsOrKeys": issues_keys
    }
    res = httpx.post(f"{self.server}/rest/api/3/bulk/issues/delete", auth=self.auth, json=payload)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def getBulkFields(self, issues_keys: list[str]) -> list[dict[str,Any]]:
    params: dict[str,Any] = {
      "issueIdsOrKeys": f"{','.join(issues_keys)}"
    }
    end = False
    all_fields: list[dict[str,Any]] = []
    cursor = None
    page = 0
    while not end:
      page += 1
      # print(f"Get page {page} with cursor {cursor}", file=sys.stderr)
      if cursor is not None:
        params['startingAfter'] = cursor
      res = httpx.get(f"{self.server}/rest/api/3/bulk/issues/fields", headers=self.headers, auth=self.auth, params=params)
      if res.status_code >= 200 and res.status_code < 300:
        raw = json.loads(res.text)
        current_fields = raw['fields']
        all_fields.extend(current_fields)
        if 'startingAfter' in raw:
          cursor = raw['startingAfter']
        else:
          cursor = None
          end = True
      else:
        print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
        return []
    return all_fields

  def editIssues(self, issues_keys: list[str], changesSet: dict[str,Any]) -> dict[str,Any]:
    payload = {
      "issueIdsOrKeys": issues_keys
    }
    res = httpx.post(f"{self.server}/rest/api/3/bulk/issues/fields", auth=self.auth, json=payload)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}
