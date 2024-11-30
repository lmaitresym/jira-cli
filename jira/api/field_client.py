from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys
# import logging

# logging.basicConfig(
#     format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logging.DEBUG
# )

def indexOf(item: Any, array: list[Any]) -> int:
    idx = 0
    for i in array:
        if str(i) == str(item):
            return idx
        idx = idx+1
    return -1

class FieldClient(JiraClient):

  def getCustomFieldById(self, id: str) -> dict[str,Any]:
    params = {
      "id": id,
      "startAt": 0,
      "maxResults": 1,
      "expand": [
        "key",
        "lastUsed",
        "screensCount",
        "contextsCount",
        "isLocked",
        "searcherKey"
      ]
    }
    res = httpx.get(f"{self.server}/rest/api/3/field/search", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return dict()

  def getFieldsByName(self, name: str) -> list[dict[str,Any]]:
    params = {
      "query": name,
      "startAt": 0,
      "maxResults": 100,
      "expand": [
        "key",
        "lastUsed",
        "screensCount",
        "contextsCount",
        "isLocked",
        "searcherKey"
      ]
    }
    res = httpx.get(f"{self.server}/rest/api/3/field/search", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return list()

  def deleteField(self, field_id: str) -> Any:
    # Works only if the field is in the trash
    res = httpx.delete(f"{self.server}/rest/api/3/field/{field_id}", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)

  def trashField(self, field_id: str) -> Any:
    res = httpx.post(f"{self.server}/rest/api/3/field/{field_id}/trash", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)

  def restoreField(self, field_id: str) -> Any:
    res = httpx.post(f"{self.server}/rest/api/3/field/{field_id}/restore", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)

  def getFields(self) -> list[dict[str,Any]]:
    res = httpx.get(f"{self.server}/rest/api/3/field", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return list()

  def createCustomField(self,
                        name: str,
                        description: str,
                        searcherKey: str,
                        fieldType: str
                        ) -> Any:
    payload = {
      "description": description,
      "name": name,
      "searcherKey": searcherKey,
      "type": fieldType
    }
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    res = httpx.post(f"{self.server}/rest/api/3/field", headers=headers, json=payload, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def createCustomFieldContext(self,
                                fieldId: str,
                                description: str,
                                issueTypeIds: list[str],
                                name: str,
                                projectIds: list[str]
                              ) -> Any:
    payload = {
      "description": description,
      "issueTypeIds": issueTypeIds,
      "name": name,
      "projectIds": projectIds
    }
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    res = httpx.post(f"{self.server}/rest/api/3/field/{fieldId}/context", headers=headers, json=payload, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def deleteCustomFieldContext(self,
                                fieldId: str,
                                contextId: str
                              ) -> Any:
    res = httpx.delete(f"{self.server}/rest/api/3/field/{fieldId}/context/{contextId}", headers=self.headers, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getReferenceData(self, field_key: str) -> Any:
    params = {
      'fieldName': field_key
    }
    res = httpx.get(f"{self.server}/rest/api/3/jql/autocompletedata", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getSuggestions(self, field_key: str) -> Any:
    params = {
      'fieldName': field_key
    }
    res = httpx.get(f"{self.server}/rest/api/3/jql/autocompletedata/suggestions", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getFieldContexts(self, field_key: str) -> Any:
    res = httpx.get(f"{self.server}/rest/api/3/field/{field_key}/context", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getFieldIdFromKeyAndMeta(self, field_key: str, issue_meta: dict[str, Any]) -> Any:
    fields = issue_meta['projects'][0]['issuetypes'][0]['fields']
    for f in fields:
      field = fields[f]
      if field['key'] == field_key:
        #print("Found field %s, return %s" % (field_key, f))
        return f
    #print("Didn't found key for %s" % field_key)
    return None
