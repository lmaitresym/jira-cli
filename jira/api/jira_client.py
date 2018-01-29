import requests
import json
import os
import base64
import glob
from lxml import etree
from pip._vendor.requests.api import head
from requests.auth import HTTPBasicAuth
from numbers import Number


class JiraClient:

    def __init__(self, configuration):
        self.configuration = configuration
        self.url = None
        if configuration is not None and 'url' in configuration:
            self.url = configuration['url']
        self.session = None
        self.platform_session = None
        #self.enableLogging()

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
        payload = {
            'username': username,
            'password': password
        }

        r = requests.post(url + '/rest/auth/1/session', json=payload, headers={
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        })

        if r.status_code == 200:
            cookies = requests.utils.dict_from_cookiejar(r.cookies)
            self.configuration['url'] = url
            self.configuration['cookies'] = cookies
            self.configuration['username'] = username
            self.configuration['password'] = password

        return r.status_code

    def logout(self):
        r = requests.delete(self.url + '/rest/auth/1/session')
        return r.status_code

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

    def updateFieldOption(self, field_key, option):
        basicAuth = HTTPBasicAuth(self.configuration['username'],self.configuration['password'])
        r = requests.put(self.url + '/rest/api/2/field/' + field_key + '/option/' + str(option['id']), auth=basicAuth, json=option)
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

# PUT /rest/api/2/issue/{issueIdOrKey}?notifyUsers=false
# 
    def updateIssue(self, issue_key, field_key, value):
        payload = {
            "update": {
                "fields": {}
            }
        }
        payload['update']['fields']
        pass

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
                print("Found field %s, return %s" % (field_key, f))
                return f
        print("Didn't found key for %s" % field_key)
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