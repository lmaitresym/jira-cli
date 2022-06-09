# -*- coding: utf-8 -*-
"""The space command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Space(Base):
    """Manage space"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getSpace()
        elif self.hasOption('list'):
            self.getList()
        else:
            print("Nothing to do.")

    def getSpace(self):
        space_key = self.options['<space_key>']
        rc, datas = self.jira_client.getSpace(space_key)
        self.processResults(rc, datas)

    def getList(self):
        rc, datas = self.jira_client.getSpace()
        self.processResults(rc, datas)
