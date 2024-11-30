from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class IssueClient(JiraClient):

  def getIssue(self, issue_key: str, fields: str) -> dict[str, Any]:
    params = {
      "fields": fields
    }
    res = httpx.get(f"{self.server}/rest/api/3/issue/{issue_key}", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def deleteIssue(self, issue_key: str) -> Any:
    res = httpx.delete(f"{self.server}/rest/api/3/issue/{issue_key}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getIssues(self, jql: str, page_size: int, fields: str) -> list[dict[str,Any]]:
    uri = f"{self.server}/rest/api/3/search"
    total = 999999
    startAtIdx = 0
    rc = 0
    maxResults = page_size
    params = { 
      "jql": jql,
      "fields": fields,
      "maxResults": maxResults
    }
    all_issues: list[dict[str,Any]] = list()
    error_message = None
    while startAtIdx < total:
      #print(f"At index {startAtIdx}/{total}...", file=sys.stderr)
      params['startAt'] = startAtIdx
      res = httpx.get(uri, params=params, auth=self.auth)
      rc = res.status_code
      if rc == 200:
        payload = json.loads(res.text)
        issues = payload['issues']
        nb_issues = len(issues)
        all_issues = all_issues + issues
        total = payload['total']
        #print(f"Got {nb_issues} issues...", file=sys.stderr)
        if startAtIdx < total:
          startAtIdx = startAtIdx + nb_issues
      else:
        error_message = res.text
        break
    if rc != 200:
      # print(f"{rc}:{error_message}", sys.stderr)
      print(f"Error: {rc}:{error_message}", file=sys.stderr)
      return []
    # pass
    return all_issues

  def getIssuesPage(self, jql: str, page: int, pageSize: int, expand: list[str]) -> Any:
    params: dict[str,Any] = {
      "jql": jql,
      "fields": "*all",
      "startAt": page*pageSize,
      "maxResults": pageSize
    }
    if expand:
      params['expand'] = expand
    res = httpx.get(f"{self.server}/rest/api/3/search", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def updateIssue(self, issue_key: str, field_key: str, value: str) -> Any:
    payload: dict[str, Any] = { "fields": {} }
    payload['fields'][field_key] = value
    res = httpx.put(f"{self.server}/rest/api/3/issue/{issue_key}", json=payload, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def createIssue(self, issue: str) -> Any:
    res = httpx.post(f"{self.server}/rest/api/3/issue", auth=self.auth, json=issue)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def createIssues(self, issues: str) -> Any:
    res = httpx.post(f"{self.server}/rest/api/3/issue/bulk", auth=self.auth, json=issues)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None
