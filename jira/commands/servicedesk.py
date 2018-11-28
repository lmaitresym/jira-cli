# -*- coding: utf-8 -*-
"""The servicedesk command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class ServiceDesk(Base):
    """Manage servicedesk"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getServiceDesk()
        elif self.hasOption('list'):
            self.listServiceDesks()
        else:
            print("Nothing to do.")

    def getServiceDesk(self):
        servicedesk_id = self.options['<servicedesk_id>']
        rc, datas = self.jira_client.getServiceDesk(servicedesk_id)
        self.processResults(rc, datas)

    def listServiceDesks(self):
        rc, datas = self.jira_client.listServiceDesks()
        self.processResults(rc, datas)
