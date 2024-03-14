# -*- coding: utf-8 -*-
"""The session command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Task(Base):
    """Manage tasks"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('cancel'):
            self.cancelTask()
        elif self.hasOption('get'):
            self.getTask()
        else:
            print("Nothing to do.")

    def getTask(self):
        task_id = self.options['<task_id>']
        rc, datas = self.jira_client.getTask(task_id)
        self.processResults(rc, datas)

    def cancelTask(self):
        task_id = self.options['<task_id>']
        rc, datas = self.jira_client.cancelTask(task_id)
        self.processResults(rc, datas)
