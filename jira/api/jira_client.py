import requests
import json
from requests.auth import HTTPBasicAuth


class JiraClient:

    def __init__(self, configuration):
        self.configuration = configuration
        self.url = None
        if configuration is not None and 'url' in configuration:
            self.url = configuration['url']
        self.session = None
        # self.enableLogging()

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

    def login(self, url, username, password):
        self.configuration['url'] = url
        self.configuration['username'] = username
        self.configuration['password'] = password
        return 200

    def logout(self):
        #basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        #r = requests.delete(self.url + '/rest/auth/1/session', auth=basicAuth)
        return 500

    def dump(self):
        return self.configuration

    def getFields(self):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/api/2/field', auth=basicAuth)
        return r.status_code, r.content

    def getReferenceData(self, field_key):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        params = {
            'fieldName': field_key
        }
        r = requests.get(self.url + '/rest/api/3/jql/autocompletedata', params=params, auth=basicAuth)
        return r.status_code, r.content

    def getSuggestions(self, field_key):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        params = {
            'fieldName': field_key
        }
        r = requests.get(self.url + '/rest/api/3/jql/autocompletedata/suggestions', params=params, auth=basicAuth)
        return r.status_code, r.content

    def getFieldOption(self, field_key, option_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/api/2/field/' + field_key + '/option/' + str(option_id), auth=basicAuth)
        return r.status_code, r.content

    def deleteFieldOption(self, field_key, option_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.delete(self.url + '/rest/api/2/field/' + field_key + '/option/' + str(option_id), auth=basicAuth)
        return r.status_code, r.text

    def getFieldOptions(self, field_key):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/api/2/field/' + field_key + '/option?maxResults=1000', auth=basicAuth)
        return r.status_code, r.content

    def addOption(self, field_key, option):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.post(self.url + '/rest/api/2/field/' + field_key + '/option', auth=basicAuth, json=option)
        return r.status_code, r.content

    def addOptionWithId(self, field_key, option, option_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.put(self.url + '/rest/api/2/field/' + field_key + '/option/' + option_id, auth=basicAuth, json=option)
        return r.status_code, r.content

    def updateFieldOption(self, field_key, option):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.put(self.url + '/rest/api/2/field/' + field_key + '/option/' + str(option['id']), auth=basicAuth, json=option)
        return r.status_code, r.content

    def replaceOption(self, field_key, option_to_replace, option_to_use, jql_filter):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        params = {
            'replaceWith': option_to_use,
            'jql': jql_filter
            }
        r = requests.delete(self.url + '/rest/api/2/field/' + field_key + '/option/' + option_to_replace + '/issue',
                            auth=basicAuth,
                            params=params)
        if r.status_code == 303:
            print('Get task status here: %s' % r.content)
        return r.status_code, r.content

    def manageOptionsForProject(self, field_key, project_id, verb):
        return

    def addProjectToFieldOptions(self, field_key, project_id):
        return

    def getIssue(self, issue_key):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/api/2/issue/' + issue_key, auth=basicAuth)
        return r.status_code, r.content

    def deleteIssue(self, issue_key):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.delete(self.url + '/rest/api/2/issue/' + issue_key, auth=basicAuth)
        return r.status_code, r.content

    def getIssues(self, jql):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        params = dict(jql=jql,fields='*all')
        r = requests.get(self.url + '/rest/api/2/search', params=params, auth=basicAuth)
        return r.status_code, r.content

    def getIssuesPage(self, jql, page, pageSize, expand=None):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        params = dict(jql=jql,fields='*all',startAt=page*pageSize,maxResults=pageSize)
        if expand is not None:
            params['expand'] = expand
        r = requests.get(self.url + '/rest/api/2/search', params=params, auth=basicAuth)
        #print(r.content)
        #print(params)
        return r.status_code, r.content

    def updateIssue(self, issue_key, field_key, value):
        payload = dict(fields=dict())
        payload['fields'][field_key] = value
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.put(self.url + '/rest/api/2/issue/' + issue_key, json=payload, auth=basicAuth)
        return r.status_code, r.content

    def getCreateMeta(self, project_key, issuetype_key):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        projectParameter = None
        try:
            projectParameter = 'projectIds=%d' % int(project_key)
        except ValueError:
            projectParameter = 'projectKeys=%s' % str(project_key)
        issueTypeParameter = None
        try:
            issueTypeParameter = 'issuetypeIds=%s' % int(issuetype_key)
        except ValueError:
            issueTypeParameter = 'issuetypeNames=%s' % str(issuetype_key)
        createMetaURL = self.url + '/rest/api/2/issue/createmeta?expand=projects.issuetypes.fields&' + projectParameter + '&' + issueTypeParameter
        #print("URL: %s" % createMetaURL)
        r = requests.get(createMetaURL, auth=basicAuth)
        return r.status_code, r.content

    def getFieldIdFromKeyAndMeta(self, field_key, issue_meta):
        #print('Type: ' + str(type(issue_meta)))
        #print(issue_meta)
        fields = issue_meta['projects'][0]['issuetypes'][0]['fields']
        for f in fields:
            field = fields[f]
            if field['key'] == field_key:
                #print("Found field %s, return %s" % (field_key, f))
                return f
        #print("Didn't found key for %s" % field_key)
        return None

    def hasOption(self, field_key, option_value):
        rc, datas = self.getFieldOptions(field_key)
        allOptions = json.loads(datas)['values']
        allValues = []
        for option in allOptions:
            allValues.append(option['value'].encode('utf-8'))
        return self.indexOf(option_value, allValues) > -1

    def indexOf(self, item, array):
        idx = 0
        for i in array:
            if str(i) == str(item):
                return idx
            idx = idx+1
        return -1

    def getProject(self, project_key_or_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/api/2/project/' + project_key_or_id, auth=basicAuth)
        return r.status_code, r.content

    def listProjects(self):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/api/2/project', auth=basicAuth)
        return r.status_code, r.content

    def getRole(self, project_id, role_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/api/2/project/' + project_id + '/role/' + role_id, auth=basicAuth)
        return r.status_code, r.content

    def getServiceDesk(self, servicedesk_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/servicedeskapi/servicedesk/' + servicedesk_id, auth=basicAuth)
        return r.status_code, r.content

    def listServiceDesks(self):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.get(self.url + '/rest/servicedeskapi/servicedesk', auth=basicAuth)
        return r.status_code, r.content

    def createIssue(self, issue):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.post(self.url + '/rest/api/2/issue', auth=basicAuth, json=issue)
        return r.status_code, r.content

    def createIssues(self, issues):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.post(self.url + '/rest/api/2/issue/bulk', auth=basicAuth, json=issues)
        return r.status_code, r.content

    def deletePage(self, page_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        headers = {
            "Accept": "application/json"
        }
        r = requests.delete(self.url + 'wiki/rest/api/content/' + page_id, headers=headers, auth=basicAuth)
        return r.status_code, r.content

    def getPage(self, space_key, page_title):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        headers = {
            "Accept": "application/json"
        }
        r = requests.get(self.url + 'wiki/rest/api/content?type=page&expand=body.editor&spaceKey=' + space_key + '&title=' + page_title, headers=headers, auth=basicAuth)
        return r.status_code, r.content

    def getPageVersion(self, space_key, page_title):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        headers = {
            "Accept": "application/json"
        }
        r = requests.get(self.url + 'wiki/rest/api/content?type=page&expand=version&spaceKey=' + space_key + '&title=' + page_title, headers=headers, auth=basicAuth)
        page = json.loads(r.content)['results'][0]
        return page

    def createPage(self, page_title, space_key, page_content, parent_id):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        payload = {
            'type': 'page',
            'title': page_title,
            'space': {
                'key': space_key
            },
            'ancestors': [{'id': parent_id}],
            'body': {
                'storage': {
                    'value': page_content,
                    'representation': 'storage'
                }
            }
        }
        r = requests.post(self.url + 'wiki/rest/api/content', auth=basicAuth, json=payload)
        return r.status_code, r.content

    def updatePage(self, page_title, space_key, page_content):
        currentPageVersion = self.getPageVersion(space_key, page_title)
        new_version = int(currentPageVersion['version']['number']) + 1
        page_id = currentPageVersion['id']
        #print("Version:{} Id:{}".format(new_version,page_id))
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
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
            }
        }
        r = requests.put(self.url + 'wiki/rest/api/content/' + page_id, auth=basicAuth, json=payload)
        return r.status_code, r.content
