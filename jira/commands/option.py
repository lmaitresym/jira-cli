# -*- coding: utf-8 -*-
"""The session command."""

import json
from .base import Base
from jira.api.jira_client import JiraClient


class Option(Base):
    """Manage options"""

    def run(self):
        #print('You supplied the following options:', json.dumps(self.options, indent=2, sort_keys=True))
        self.jira_client = JiraClient(self.loadConfiguration())
        if self.hasOption('get'):
            self.getOption()
        elif self.hasOption('add'):
            self.addOption()
        elif self.hasOption('del'):
            self.deleteOption()
        else:
            print("Nothing to do.")

    def getOption(self):
        field_key = self.options['<field_key>']
        option_id = self.options['<option_id>']
        rc, datas = self.jira_client.getFieldOption(field_key, option_id)
        self.processResults(rc, datas)

    def deleteOption(self):
        field_key = self.options['<field_key>']
        option_id = self.options['<option_id>']
        if str(option_id).find('..') == -1:
            rc, datas = self.jira_client.deleteFieldOption(field_key, option_id)
            if rc != 204:
                try:
                    print(json.dumps(json.loads(datas), indent=2))
                except:
                    print(datas)
                self.processResults(rc, datas)
        else:
            options_limits = str(option_id).split('..')
            option_low = int(options_limits[0])
            option_high = int(options_limits[1])
            for opt in range(option_low, option_high):
                rc, datas = self.jira_client.deleteFieldOption(field_key, opt)
                if rc != 204:
                    try:
                        print(json.dumps(json.loads(datas), indent=2))
                    except:
                        print(datas)

    def addOption(self):
        pass

    def indexOf(self, item, array):
        idx = 0
        for i in array:
            if str(i) == str(item):
                return idx
            idx = idx+1
        return -1
