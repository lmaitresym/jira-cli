# -*- coding: utf-8 -*-
"""The session command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Session(Base):
    """Manage sessions"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('login'):
            self.login()
        elif self.hasOption('logout'):
            self.logout()
        else:
            print("Nothing to do.")

    def login(self):
        url = self.options['<url>']
        username = self.options['<username>']
        password = self.options['<password>']

        rc = self.jira_client.login(url, username, password)

        if rc == 200:
            self.saveConfiguration(self.jira_client.getConfiguration())
        self.processResultCode(rc)

    def logout(self):
        rc = self.jira_client.logout()
        self.processResultCode(rc)

