# -*- coding: utf-8 -*-
"""Relabel pages."""

from jira.api.jira_client import JiraClient
import json
import os
import pickle

if __name__ == "__main__":

    page_id = '782699699'
    new_label = 'scrum_reports'

    configurationPath = os.environ['HOME'] + '/.jira'
    if os.path.exists(configurationPath):
        with open(configurationPath,'rb') as f:
            configuration = pickle.load(f)
    else:
        configuration = dict()
    jiraClient = JiraClient(configuration)

    all_page_children = jiraClient.getAllPageChildrenById(page_id)
    all_page_children_len = len(all_page_children)
    print('Adding label {} to {} children pages of page with id {}.'.format(new_label,all_page_children_len,page_id))
    for idx, child in enumerate(all_page_children):
        print('{}/{}'.format((idx+1),all_page_children_len))
        status_code, result = jiraClient.addPageLabelById(child['id'],new_label)
