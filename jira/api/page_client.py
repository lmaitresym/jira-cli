from jira.api.jira_client import JiraClient
import httpx
import json
from typing import Any
import sys

class PageClient(JiraClient):

  def deletePage(self, page_id: str) -> Any:
    res = httpx.delete(f"{self.server}/wiki/rest/api/content/{page_id}", headers=self.headers, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getPage(self, space_key: str, page_title: str) -> dict[str,Any]:
    params = {
      "type": "page",
      "expand": "body.editor",
      "spaceKey": space_key,
      "title": page_title
    }
    res = httpx.get(f"{self.server}/wiki/rest/api/content", headers=self.headers, params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return {}

  def getPageVersion(self, space_key: str, page_title: str) -> Any:
    params = {
      "type": "page",
      "expand": "version",
      "spaceKey": space_key,
      "title": page_title
    }
    res = httpx.get(f"{self.server}/wiki/rest/api/content", headers=self.headers, params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
      page = json.loads(res.text)['results'][0]
      return page
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def createPage(self, page_title: str, space_key: str, page_content: Any, parent_id: str, labels: list[str] = list()) -> Any:
    payload = {
      'type': 'page',
      'title': page_title,
      'space': {
        'key': space_key
      },
      'ancestors': [
        {'id': parent_id}
      ],
      'body': {
        'storage': {
          'value': page_content,
          'representation': 'storage'
        }
      },
      'metadata': {
        'labels': labels
      }
    }
    res = httpx.post(f"{self.server}/wiki/rest/api/content", auth=self.auth, json=payload)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def updatePage(self, page_title: str, space_key: str, page_content: Any, labels: list[str] = list()) -> Any:
    currentPageVersion = self.getPageVersion(space_key, page_title)
    new_version = int(currentPageVersion['version']['number']) + 1
    page_id = currentPageVersion['id']
    payload = {
      'type': 'page',
      'version': {
        'number': new_version
      },
      'title': page_title,
      'space': {
        'key': space_key
      },
      'body': {
        'storage': {
          'value': page_content,
          'representation': 'storage'
        }
      },
      'metadata': {
        'labels': labels
      }
    }
    res = httpx.put(f"{self.server}/wiki/rest/api/content/{page_id}", auth=self.auth, json=payload)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def movePage(self, page_title: str, space_key: str, parent_id: str) -> Any:
    current_page = self.getPageVersion(space_key, page_title)
    version = int(current_page['version']['number']) + 1
    title = current_page['title']
    type = current_page['type']
    page_id = current_page['id']
    payload = {
      'type': type,
      'title': title,
      'version': {
        'number': version
      },
      'ancestors': [{'id': parent_id}]
    }
    res = httpx.put(f"{self.server}/wiki/rest/api/content/{page_id}", auth=self.auth, json=payload)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getPageLabels(self, page_title: str, space_key: str) -> Any:
    current_page = self.getPageVersion(space_key, page_title)
    page_id = current_page['id']
    return self.getPageLabelsById(page_id)

  def getPageLabelsById(self, page_id: str) -> Any:
    res = httpx.get(f"{self.server}/wiki/rest/api/content/{page_id}/label", auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)['results']
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def addPageLabel(self, page_title: str, space_key: str, label: str) -> Any:
    current_page = self.getPageVersion(space_key, page_title)
    id = current_page['id']
    return self.addPageLabelById(id, label)

  def addPageLabelById(self, page_id: str, label: str) -> Any:
    payload = [
      {
        'prefix': 'global',
        'name': label
      }
    ]
    res = httpx.post(f"{self.server}/wiki/rest/api/content/{page_id}/label", auth=self.auth, json=payload)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getPageChildrenById(self, page_id: str) -> Any:
    params = { 'expand': 'page' }
    res = httpx.get(f"{self.server}/wiki/rest/api/content/{page_id}/child", params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)['page']['results']
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getPageChildren(self, page_title: str, space_key: str) -> Any:
    current_page = self.getPageVersion(space_key, page_title)
    id = current_page['id']
    return self.getPageChildrenById(id)

  def getAllPageChildren(self, page_title: str, space_key: str) -> list[Any]:
    current_page = self.getPageVersion(space_key, page_title)
    id = current_page['id']
    return self.getAllPageChildrenById(id)

  def getAllPageChildrenById(self, page_id: str) -> Any:
    children = self.getPageChildrenById(page_id)
    allChildren = list(children)
    for child in children:
      child_children = self.getPageChildrenById(child['id'])
      allChildren.extend(child_children)
    return allChildren

  def getSpace(self, space_id: str) -> Any:
    params = { 'spaceKey': space_id }
    res = httpx.get(f"{self.server}/wiki/rest/api/space", headers=self.headers, params=params, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None

  def getSpaces(self) -> Any:
    res = httpx.get(f"{self.server}/wiki/rest/api/space", headers=self.headers, auth=self.auth)
    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.text)
    print(f"Error {res.status_code}: {res.text}", file=sys.stderr)
    return None
