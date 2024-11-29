# -*- coding: utf-8 -*-
"""The role command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Screen(Base):
    """Manage Screen"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getScreen()
        elif self.hasOption('gettabs'):
            self.getScreenTabs()
        elif self.hasOption('addFieldToTab'):
            self.addFieldToTab()
        else:
            print("Nothing to do.")

    def getScreen(self):
        screen_id = self.options['<screen_id>']
        rc, datas = self.jira_client.getScreen(screen_id)
        self.processResults(rc, datas)

    def getScreenTabs(self):
        screen_id = self.options['<screen_id>']
        project_id = self.options['<project_id>']
        rc, datas = self.jira_client.getScreenTabs(screen_id, project_id)
        self.processResults(rc, datas)

    def addFieldToTab(self):
        screen_id = self.options['<screen_id>']
        tab_id = self.options['<tab_id>']
        field_id = self.options['<field_id>']
        rc, datas = self.jira_client.addFieldToTab(screen_id, tab_id, field_id)
        self.processResults(rc, datas)

