"""The base command."""

import os
import pickle


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        try:
            self.configurationPath = os.environ['JIRA_CONFIG']
        except KeyError:
            self.configurationPath = os.environ['HOME'] + '/.jira'
        self.results = None
        self.headless = False

    def run(self):
        raise NotImplementedError(
            'You must implement the run() method yourself!')

    def loadConfiguration(self):
        if os.path.exists(self.configurationPath):
            with open(self.configurationPath,'rb') as f:
                return pickle.load(f)
        else:
            return dict()

    def saveConfiguration(self, configuration):
        with open(self.configurationPath, 'wb') as f:
            pickle.dump(configuration, f)

    def processResults(self, rc, datas):
        if self.headless:
            self.results = dict(rc=rc, datas=datas)
        else:
            if rc == 200 or rc == 204:
                print(datas.decode())
            else:
                print('KO - %d' % rc)

    def processResultCode(self, rc):
        if self.headless:
            self.results = dict(rc=rc)
        else:
            if rc == 200:
                print('OK')
            else:
                print('KO - %d' % rc)

    def hasOption(self, option):
        return option in self.options and self.options[option]

    def getOption(self, option, defaultValue=None):
        if self.hasOption(option):
            return self.options[option]
        return defaultValue

    def getResults(self):
        return self.results

    def indexOf(self, item, array):
        idx = 0
        for i in array:
            if str(i) == str(item):
                return idx
            idx = idx+1
        return -1
