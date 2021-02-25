# -*- coding: utf-8 -*-
"""The issues command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Issues(Base):
    """Manage issues"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getIssues()
        elif self.hasOption('getkeys'):
            self.getIssuesKeys()
        elif self.hasOption('create'):
            self.createIssues()
        else:
            print("Nothing to do.")

    def getIssues(self):
        jql = self.options['<jql>']
        if self.hasOption('--page'):
            page_index = int(self.options['--page'])
        else:
            page_index = 0
        if self.hasOption('--page-size'):
            page_size = int(self.options['--page-size'])
        else:
            page_size = 50
        #print("Get page %s/%s of issues for jql %s" % (page_index, page_size, jql))
        rc, datas = self.jira_client.getIssuesPage(jql, page_index, page_size)
        self.processResults(rc, datas)

    def getIssuesKeys(self):
        jql = self.options['<jql>']
        rc, datas = self.jira_client.getIssues(jql)
        issues = json.loads(datas)['issues']
        issuesKeys = list()
        for issue in issues:
            issuesKeys.append(issue['key'])
        print(json.dumps(issuesKeys))

    def createIssues(self):
        json_file = self.options['<json_file>']
        with open(json_file,'r') as issues_raw:
            issues = json.load(issues_raw)
            rc, datas = self.jira_client.createIssues(json_file)
            self.processResults(rc, datas)

