# -*- coding: utf-8 -*-
"""The issuetype command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Issue(Base):
    """Manage issues"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getIssueType()
        elif self.hasOption('getbyproject'):
            self.getIssueTypesByProject()
        elif self.hasOption('getall'):
            self.getIssueTypes()
        else:
            print("Nothing to do.")

    def getIssueType(self):
        issuetype_key = self.options['<issuetype_key>']
        rc, datas = self.jira_client.getIssueType(issuetype_key)
        self.processResults(rc, datas)

    def getIssueTypes(self):
        rc, datas = self.jira_client.getIssueTypes()
        self.processResults(rc, datas)

    def getIssueTypesByProject(self):
        project_id = self.options['<project_id>']
        rc, datas = self.jira_client.getIssueTypesByProject(project_id)
        self.processResults(rc, datas)
