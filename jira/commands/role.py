# -*- coding: utf-8 -*-
"""The role command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Role(Base):
    """Manage role"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getRole()
        else:
            print("Nothing to do.")

    def getRole(self):
        project_id = self.options['<project_id>']
        role_id = self.options['<role_id>']
        rc, datas = self.jira_client.getRole(project_id, role_id)
        self.processResults(rc, datas)
