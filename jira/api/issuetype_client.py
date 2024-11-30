from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class IssueTypeClient(JiraClient):

  def getIssueType(self, issuetype_key: str) -> dict[str, Any]:
    res = httpx.get(f"{self.server}/rest/api/3/issuetype/{issuetype_key}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def getIssueTypes(self) -> list[dict[str, Any]]:
    res = httpx.get(f"{self.server}/rest/api/3/issuetype", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return []

  def getIssueTypesByProject(self, project_id: str) -> list[dict[str, Any]]:
    params = {
      'projectId': project_id
    }
    res = httpx.get(f"{self.server}/rest/api/3/issuetype/project", auth=self.auth, params=params)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return []

  def getCreateMeta(self, project_key: Any, issuetype_key: Any) ->  dict[str, Any]:
    params: dict[str,Any] = {
      "expand": "projects.issuetypes.fields"
    }
    if isinstance(project_key, int):
      params['projectIds'] = project_key
    elif isinstance(project_key, str):
      params['projectKeys'] = project_key
    if isinstance(issuetype_key, int):
      params['issuetypeIds'] = issuetype_key
    elif isinstance(issuetype_key, str):
      params['issuetypeNames'] = issuetype_key
    res = httpx.get(f"{self.server}/rest/api/3/issue/createmeta", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}
