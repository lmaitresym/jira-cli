# -*- coding: utf-8 -*-
"""The page command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Page(Base):
    """Manage page"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getPage()
        elif self.hasOption('create'):
            self.createPage()
        elif self.hasOption('delete'):
            self.deletePage()
        else:
            print("Nothing to do.")

    def getPage(self):
        page_title = self.options['<page_title>']
        space_key = self.options['<space_key>']
        rc, datas = self.jira_client.getPage(space_key,page_title)
        self.processResults(rc, datas)

    def deletePage(self):
        page_id = self.options['<page_id>']
        rc, datas = self.jira_client.deletePage(page_id)
        self.processResults(rc, datas)

    def createPage(self):
        page_title = self.options['<page_title>']
        space_key = self.options['<space_key>']
        page_file = self.options['<page_file>']
        parent_id = self.options['<parent_id>']
        with open(page_file,'r') as page_raw:
            page_content = page_raw.read()
            rc, datas = self.jira_client.createPage(page_title, space_key, page_content, parent_id)
            self.processResults(rc, datas)
