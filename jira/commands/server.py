# -*- coding: utf-8 -*-
"""The session command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Server(Base):
    """Manage server"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('infos'):
            self.getServerInfos()
        else:
            print("Nothing to do.")

    def getServerInfos(self):
        rc, datas = self.jira_client.getServerInfos()
        self.processResults(rc, datas)
