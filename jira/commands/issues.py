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
        else:
            print("Nothing to do.")

    def getIssues(self):
        jql = self.options['<jql>']
        # print("Get issues for jql %s" % jql)
        rc, datas = self.jira_client.getIssues(jql)
        self.processResults(rc, datas)

    def getIssuesKeys(self):
        jql = self.options['<jql>']
        rc, datas = self.jira_client.getIssues(jql)
        issues = json.loads(datas)['issues']
        issuesKeys = list()
        for issue in issues:
            issuesKeys.append(issue['key'])
        print(json.dumps(issuesKeys))
