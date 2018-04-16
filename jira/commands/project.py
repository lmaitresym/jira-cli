# -*- coding: utf-8 -*-
"""The project command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Project(Base):
    """Manage project"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getProject()
        else:
            print("Nothing to do.")

    def getProject(self):
        project_key_or_id = self.options['<project_key_or_id>']
        rc, datas = self.jira_client.getProject(project_key_or_id)
        self.processResults(rc, datas)
