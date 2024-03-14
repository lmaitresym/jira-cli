# -*- coding: utf-8 -*-
"""The session command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Settings(Base):
    """Manage settings"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('list'):
            self.listSettings()
        elif self.hasOption('get'):
            self.getSetting()
        elif self.hasOption('set'):
            self.setSetting()
        else:
            print("Nothing to do.")

    def getSetting(self):
        setting_key = self.options['<setting_key>']
        rc, datas = self.jira_client.getSetting(setting_key)
        self.processResults(rc, datas)

    def setSetting(self):
        setting_key = self.options['<setting_key>']
        setting_value = self.options['<setting_value>']
        rc, datas = self.jira_client.setSetting(setting_key, setting_value)
        self.processResults(rc, datas)

    def listSettings(self):
        category = self.options['<category>']
        rc, datas = self.jira_client.listSettings(category)
        self.processResults(rc, datas)
