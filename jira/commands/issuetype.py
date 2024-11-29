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
        elif self.hasOption('delete'):
            self.deleteIssueType()
        elif self.hasOption('create'):
            self.createIssueType()
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

    def deleteIssueType(self):
        issuetype_id = self.options['<issuetype_id>']
        rc, datas = self.jira_client.deleteIssueType(issuetype_id)
        self.processResults(rc, datas)

    def createIssueType(self):
        issuetype_name = self.options['<issuetype_name>']
        issuetype_description = self.options['<issuetype_description>']
        issuetype_hierarchy_level = self.options['<issuetype_hierarchy_level>']
        rc, datas = self.jira_client.createIssueType(issuetype_name, issuetype_description, issuetype_hierarchy_level)
        self.processResults(rc, datas)
