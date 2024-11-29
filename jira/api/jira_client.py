import requests
import json
from requests.auth import HTTPBasicAuth
import sys

class JiraClient:

    def __init__(self, configuration):
        self.configuration = configuration
        self.url = None
        self.auth = None
        self.headless = False
        if configuration is not None:
            if 'url' in configuration:
                self.url = configuration['url']
            if 'username' in configuration and 'password' in configuration:
                self.auth = HTTPBasicAuth(configuration['username'], configuration['password'])
            if 'headless' in configuration:
                self.headless = configuration['headless']
            if 'debug' in configuration:
                self.enableLogging()
        self.headers = { "Accept": "application/json" }
        self.session = None

    def enableLogging(self):
        import logging
        import time

        try:
            import http.client as http_client
        except ImportError:
            import httplib as http_client
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('--- %s ---', time.strftime("%H:%M:%S"))

    def getConfiguration(self):
        return self.configuration

    def formatResponse(self, response):
        if response.text is not None and response.text != '':
            try:
                return [response.status_code, json.dumps(json.loads(response.text), indent=True)]
            except:
                return [response.status_code, response.text]
        return [response.status_code, None]

    # Session API

    def login(self, url: str, username: str, password: str):
        self.configuration['url'] = url
        self.configuration['username'] = username
        self.configuration['password'] = password
        return 200

    def dump(self):
        return self.configuration

    def getCustomFieldById(self, id: str):
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
        r = requests.get(f"{self.url}/rest/api/3/field/search", params=params, auth=self.auth)
        return r.status_code, r.content

    def getFieldsByName(self, name: str):
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
        r = requests.get(f"{self.url}/rest/api/3/field/search", params=params, auth=self.auth)
        return r.status_code, r.content

    def deleteField(self, field_id: str):
        # Works only if the field is in the trash
        r = requests.delete(f"{self.url}/rest/api/3/field/{field_id}", auth=self.auth)
        return r.status_code, r.content

    def trashField(self, field_id: str):
        r = requests.post(f"{self.url}/rest/api/3/field/{field_id}/trash", auth=self.auth)
        return r.status_code, r.content

    def restoreField(self, field_id: str):
        r = requests.post(f"{self.url}/rest/api/3/field/{field_id}/restore", auth=self.auth)
        return r.status_code, r.content

    def getFields(self):
        r = requests.get(f"{self.url}/rest/api/3/field", auth=self.auth)
        return r.status_code, r.content

    def getReferenceData(self, field_key: str):
        params = {
            'fieldName': field_key
        }
        r = requests.get(f"{self.url}/rest/api/3/jql/autocompletedata", params=params, auth=self.auth)
        return r.status_code, r.content

    def getSuggestions(self, field_key: str):
        params = {
            'fieldName': field_key
        }
        r = requests.get(f"{self.url}/rest/api/3/jql/autocompletedata/suggestions", params=params, auth=self.auth)
        return r.status_code, r.content

    def getFieldOption(self, field_key: str, option_id):
        r = requests.get(f"{self.url}/rest/api/3/field/{field_key}/option/{option_id}", auth=self.auth)
        return r.status_code, r.content

    def deleteFieldOption(self, field_key: str, option_id):
        r = requests.delete(f"{self.url}/rest/api/3/field/{field_key}/option/{option_id}", auth=self.auth)
        return r.status_code, r.text

    def getFieldOptions(self, field_key: str, context):
        if context is None:
            uri = f"{self.url}/rest/api/3/customFieldOption/{field_key}"
        else:
            uri = f"{self.url}/rest/api/3/field/{field_key}/context/{context}/option"

        isLast = False
        startAtIdx = 0
        maxResults = 1000
        rc = 0
        all_options = list()
        error_message = None
        while not isLast:
            params = {
                "startAt": startAtIdx,
                "maxResults": maxResults
            }
            r = requests.get(uri, params=params, auth=self.auth)
            rc = r.status_code
            if rc == 200:
                payload = json.loads(r.content)
                all_options = all_options + payload['values']
                isLast = payload['isLast']
                if not isLast:
                    startAtIdx = len(all_options)
            else:
                error_message = r.content
                break
        if rc != 200:
            return rc, error_message
        return rc, json.dumps(all_options)

    def getFieldContexts(self, field_key: str):
        r = requests.get(f"{self.url}/rest/api/3/field/{field_key}/context", auth=self.auth)
        return r.status_code, r.content

    def addOptionWithContext(self, field_key: str, context_id: str, option_value: str):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "options": [
                {
                    'disabled': False,
                    'value': option_value
                }
            ]
        })
        r = requests.post(f"{self.url}/rest/api/3/field/{field_key}/context/{context_id}/option", auth=self.auth, headers=headers, data=payload)
        return r.status_code, r.content

    def delOptionWithContext(self, field_key: str, context_id: str, option_id: str):
        r = requests.delete(f"{self.url}/rest/api/3/field/{field_key}/context/{context_id}/option/{option_id}", auth=self.auth)
        return r.status_code, r.content

    def delAllOptionsWithContext(self, field_key, context_id):
        _, options = self.getFieldOptions(field_key, context_id)
        for o in json.loads(options):
            # print(o)
            # option = options[o]
            rc, ret = self.delOptionWithContext(field_key, context_id, o['id'])
        return 200, ""

    def addOption(self, field_key: str, option: str):
        r = requests.post(f"{self.url}/rest/api/3/field/{field_key}/option", auth=self.auth, json=option)
        return r.status_code, r.content

    def addCascadingOption(self, field_key: str, contextId, parentOptionId, optionValue):
        json = {
            'options': [
                {
                    'value': optionValue,
                    'optionId': parentOptionId,
                    'disabled': False
                }
            ]
        }
        r = requests.post(f"{self.url}/rest/api/3/field/{field_key}/context/{contextId}/option", auth=self.auth, json=json)
        return r.status_code, r.content

    def delCascadingOption(self, field_key: str, contextId, parentOptionId, optionId):
        r = requests.delete(f"{self.url}/rest/api/3/field/{field_key}/context/{contextId}/option/{optionId}", auth=self.auth)
        return r.status_code, r.content

    def addOptionWithId(self, field_key: str, option, option_id):
        r = requests.put(f"{self.url}/rest/api/3/field/{field_key}/option/{option_id}", auth=self.auth, json=option)
        return r.status_code, r.content

    def updateFieldOption(self, field_key: str, option):
        r = requests.put(f"{self.url}/rest/api/3/field/{field_key}/option/{option['id']}", auth=self.auth, json=option)
        return r.status_code, r.content

    def replaceOption(self, field_key: str, option_to_replace, option_to_use, jql_filter):
        params = {
            "replaceWith": option_to_use,
            "jql": jql_filter
        }
        r = requests.delete(f"{self.url}/rest/api/3/field/{field_key}/option/{option_to_replace}/issue",
                            auth=self.auth,
                            params=params)
        if r.status_code == 303:
            print('Get task status here: %s' % r.content)
        return r.status_code, r.content

    def createCustomField(self,
                          name: str,
                          description: str,
                          searcherKey: str,
                          fieldType: str
                          ):
        json = {
            "description": description,
            "name": name,
            "searcherKey": searcherKey,
            "type": fieldType
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        r = requests.post(f"{self.url}/rest/api/3/field", headers=headers, json=json, auth=self.auth)
        return r.status_code, r.content

    def createCustomFieldContext(self,
                                 fieldId: str,
                                 description: str,
                                 issueTypeIds: list[str],
                                 name: str,
                                 projectIds: list[str]
                                ):
        json = {
            "description": description,
            "issueTypeIds": issueTypeIds,
            "name": name,
            "projectIds": projectIds
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        r = requests.post(f"{self.url}/rest/api/3/field/{fieldId}/context", headers=headers, json=json, auth=self.auth)
        return r.status_code, r.content

    def deleteCustomFieldContext(self,
                                 fieldId: str,
                                 contextId: str
                                ):
        r = requests.delete(f"{self.url}/rest/api/3/field/{fieldId}/context/{contextId}", headers=self.headers, auth=self.auth)
        return r.status_code, r.content

    def getIssue(self, issue_key, fields):
        params = {
            "fields": fields
        }
        r = requests.get(f"{self.url}/rest/api/3/issue/{issue_key}", params=params, auth=self.auth)
        return r.status_code, r.content

    def deleteIssue(self, issue_key: str):
        r = requests.delete(f"{self.url}/rest/api/3/issue/{issue_key}", auth=self.auth)
        return r.status_code, r.content

    def getIssues(self, jql: str, page_size: int, fields: str):
        uri = f"{self.url}/rest/api/3/search"
        total = 999999
        startAtIdx = 0
        rc = 0
        maxResults = page_size
        params = { 
            "jql": jql,
            "fields": fields,
            "maxResults": maxResults
        }

        all_issues = list()
        error_message = None
        while startAtIdx < total:
            #print(f"At index {startAtIdx}/{total}...", file=sys.stderr)
            params['startAt'] = startAtIdx
            r = requests.get(uri, params=params, auth=self.auth)
            rc = r.status_code
            if rc == 200:
                payload = json.loads(r.content)
                issues = payload['issues']
                nb_issues = len(issues)
                all_issues = all_issues + issues
                total = payload['total']
                #print(f"Got {nb_issues} issues...", file=sys.stderr)
                if startAtIdx < total:
                    startAtIdx = startAtIdx + nb_issues
            else:
                error_message = r.content
                break
        if rc != 200:
            # print(f"{rc}:{error_message}", sys.stderr)
            print(f"{rc}:{error_message}", file=sys.stderr)
            # pass
            return rc, error_message
        # pass
        return rc, json.dumps(all_issues, indent=True)

    def getIssuesPage(self, jql: str, page, pageSize, expand=None):
        params = {
            "jql": jql,
            "fields": "*all",
            "startAt": page*pageSize,
            "maxResults": pageSize
        }
        if expand is not None:
            params['expand'] = expand
        r = requests.get(f"{self.url}/rest/api/3/search", params=params, auth=self.auth)
        return r.status_code, r.content

    def updateIssue(self, issue_key: str, field_key: str, value):
        payload = { "fields": {} }
        payload['fields'][field_key] = value
        r = requests.put(f"{self.url}/rest/api/3/issue/{issue_key}", json=payload, auth=self.auth)
        return r.status_code, r.content

    def getCreateMeta(self, project_key: str, issuetype_key: str):
        params = {
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
        r = requests.get(f"{self.url}/rest/api/3/issue/createmeta", params=params, auth=self.auth)
        return r.status_code, r.content

    def getFieldIdFromKeyAndMeta(self, field_key: str, issue_meta: str):
        fields = issue_meta['projects'][0]['issuetypes'][0]['fields']
        for f in fields:
            field = fields[f]
            if field['key'] == field_key:
                #print("Found field %s, return %s" % (field_key, f))
                return f
        #print("Didn't found key for %s" % field_key)
        return None

    def hasOption(self, field_key: str, option_value):
        rc, datas = self.getFieldOptions(field_key)
        allOptions = json.loads(datas)['values']
        allValues = []
        for option in allOptions:
            allValues.append(option['value'].encode('utf-8'))
        return self.indexOf(option_value, allValues) > -1

    def indexOf(self, item: str, array: list[str]):
        idx = 0
        for i in array:
            if str(i) == str(item):
                return idx
            idx = idx+1
        return -1

    def getProject(self, project_key_or_id: str):
        params = {
            "expand": [
                "description",
                "issueTypes",
                "lead",
                "projectKeys",
                "issueTypeHierarchy"
            ]
        }
        r = requests.get(f"{self.url}/rest/api/3/project/{project_key_or_id}", params=params, auth=self.auth)
        return r.status_code, r.content

    def listProjects(self):
        r = requests.get(f"{self.url}/rest/api/3/project", auth=self.auth)
        return r.status_code, r.content

    def getRole(self, project_id: str, role_id: str):
        r = requests.get(f"{self.url}/rest/api/3/project/{project_id}/role/{role_id}", auth=self.auth)
        return r.status_code, r.content

    def getServiceDesk(self, servicedesk_id: str):
        r = requests.get(f"{self.url}/rest/servicedeskapi/servicedesk/{servicedesk_id}", auth=self.auth)
        return r.status_code, r.content

    def listServiceDesks(self):
        r = requests.get(f"{self.url}/rest/servicedeskapi/servicedesk", auth=self.auth)
        return r.status_code, r.content

    def createIssue(self, issue):
        r = requests.post(f"{self.url}/rest/api/3/issue", auth=self.auth, json=issue)
        return r.status_code, r.content

    def createIssues(self, issues):
        r = requests.post(f"{self.url}/rest/api/3/issue/bulk", auth=self.auth, json=issues)
        return r.status_code, r.content

    def deletePage(self, page_id: str):
        r = requests.delete(f"{self.url}/wiki/rest/api/content/{page_id}", headers=self.headers, auth=self.auth)
        return r.status_code, r.content

    def getPage(self, space_key: str, page_title: str):
        params = {
            "type": "page",
            "expand": "body.editor",
            "spaceKey": space_key,
            "title": page_title
        }
        r = requests.get(f"{self.url}/wiki/rest/api/content", headers=self.headers, params=params, auth=self.auth)
        return r.status_code, r.content

    def getPageVersion(self, space_key: str, page_title: str):
        params = {
            "type": "page",
            "expand": "version",
            "spaceKey": space_key,
            "title": page_title
        }
        r = requests.get(f"{self.url}/wiki/rest/api/content", headers=self.headers, params=params, auth=self.auth)
        page = json.loads(r.content)['results'][0]
        return page

    def createPage(self, page_title: str, space_key: str, page_content, parent_id: str, labels=list()):
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
        r = requests.post(f"{self.url}/wiki/rest/api/content", auth=self.auth, json=payload)
        return r.status_code, r.content

    def updatePage(self, page_title: str, space_key: str, page_content, labels=list()):
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
        r = requests.put(f"{self.url}/wiki/rest/api/content/{page_id}", auth=self.auth, json=payload)
        return r.status_code, r.content

    def movePage(self, page_title: str, space_key: str, parent_id: str):
        current_page = self.getPageVersion(space_key, page_title)
        id = current_page['id']
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
        r = requests.put(f"{self.url}/wiki/rest/api/content/{page_id}", auth=self.auth, json=payload)
        return r.status_code, r.content

    def getPageLabels(self, page_title: str, space_key: str):
        current_page = self.getPageVersion(space_key, page_title)
        page_id = current_page['id']
        return self.getPageLabelsById(page_id)

    def getPageLabelsById(self, page_id: str):
        r = requests.get(f"{self.url}/wiki/rest/api/content/{page_id}/label", auth=self.auth)
        if r.status_code != 200:
            return []
        return json.loads(r.content)['results']

    def addPageLabel(self, page_title: str, space_key: str, label: str):
        current_page = self.getPageVersion(space_key, page_title)
        id = current_page['id']
        return self.addPageLabelById(id, label)

    def addPageLabelById(self, page_id, label):
        current_labels = self.getPageLabelsById(page_id)
        payload = [
            {
                'prefix': 'global',
                'name': label
            }
        ]
        r = requests.post(f"{self.url}/wiki/rest/api/content/{page_id}/label", auth=self.auth, json=payload)
        return r.status_code, r.content

    def getPageChildrenById(self, page_id: str):
        params = { 'expand': 'page' }
        r = requests.get(f"{self.url}/wiki/rest/api/content/{page_id}/child", params=params, auth=self.auth)
        if r.status_code != 200:
            return []
        return json.loads(r.content)['page']['results']

    def getPageChildren(self, page_title: str, space_key: str):
        current_page = self.getPageVersion(space_key, page_title)
        id = current_page['id']
        return self.getPageChildrenById(id)

    def getAllPageChildren(self, page_title: str, space_key: str):
        current_page = self.getPageVersion(space_key, page_title)
        id = current_page['id']
        return self.getAllPageChildrenById(id)

    def getAllPageChildrenById(self, page_id: str):
        children = self.getPageChildrenById(page_id)
        allChildren = list(children)
        for child in children:
            child_children = self.getPageChildrenById(child['id'])
            allChildren.extend(child_children)
        return allChildren

    def getSpace(self, space_id: str):
        params = { 'spaceKey': space_id }
        r = requests.get(f"{self.url}/wiki/rest/api/space", headers=self.headers, params=params, auth=self.auth)
        return r.status_code, r.content

    def getTask(self, task_id: str):
        r = requests.get(f"{self.url}/rest/api/3/task/{task_id}", headers=self.headers, auth=self.auth)
        return r.status_code, r.content

    def cancelTask(self, task_id: str):
        r = requests.get(f"{self.url}/rest/api/3/task/{task_id}/cancel", headers=self.headers, auth=self.auth)
        return r.status_code, r.content

    def getServerInfos(self):
        r = requests.get(f"{self.url}/rest/api/3/serverInfo", auth=self.auth)
        return r.status_code, r.content

    def getSetting(self, setting_key: str):
        params = {
            "key": setting_key
        }
        r = requests.get(f"{self.url}/rest/api/3/application-properties", params=params, auth=self.auth)
        return r.status_code, r.content

    def setSetting(self, setting_key: str, setting_value: str):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "id": setting_key,
            "value": setting_value
        })
        r = requests.put(f"{self.url}/rest/api/3/application-properties/{setting_key}", data=payload, headers=headers, auth=self.auth)
        return r.status_code, r.content

    def listSettings(self, category: str):
        if category == 'global':
            r = requests.get(f"{self.url}/rest/api/3/configuration", auth=self.auth)
        elif category == 'advanced':
            r = requests.get(f"{self.url}/rest/api/3/application-properties/advanced-settings", auth=self.auth)
        else:
            r = requests.get(f"{self.url}/rest/api/3/application-properties", auth=self.auth)
        return r.status_code, r.content

    def getIssueType(self, issuetype_key: str):
        r = requests.get(f"{self.url}/rest/api/3/issuetype/{issuetype_key}", auth=self.auth)
        return r.status_code, r.content

    def getIssueTypes(self):
        r = requests.get(f"{self.url}/rest/api/3/issuetype", auth=self.auth)
        return r.status_code, r.content

    def getIssueTypesByProject(self, project_id: str):
        params = {
            'projectId': project_id
        }
        r = requests.get(f"{self.url}/rest/api/3/issuetype/project", auth=self.auth, params=params)
        return r.status_code, r.content

    def getScreen(self, screen_id: str):
        params = {
            'id': [ 
                int(screen_id)
            ]
        }
        r = requests.get(f"{self.url}/rest/api/3/screens", auth=self.auth, params=params)
        return r.status_code, r.content

    def getScreenTabs(self, screen_id: str, project_id: str):
        params = {
            'projectKey': project_id
        }
        r = requests.get(f"{self.url}/rest/api/2/screens/{screen_id}/tabs", auth=self.auth, params=params)
        return r.status_code, r.content

    def addFieldToTab(self, screen_id: str, tab_id: str, field_id: str):
        payload = {
            'fieldId': field_id
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        r = requests.post(f"{self.url}/rest/api/2/screens/{screen_id}/tabs/{tab_id}/fields", headers=headers, auth=self.auth, data=json.dumps(payload))
        return r.status_code, r.content
