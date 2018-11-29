#!/usr/bin/python

import json

files = [
    "application_options.json",
    "classeDemande_options.json",
    "classeService_options.json",
    "department_options.json",
    "impact_options.json",
    "incident_options.json",
    "origin_options.json",
    "produit_options.json",
    "server_options.json",
    "service_options.json",
    "sousProduit_options.json",
    "timenet_options.json",
    "typeIncident_options.json",
    "urgency_options.json"
    ]

# {u'config': {u'scope': {u'projects2': [{u'attributes': [], u'id': 19802}], u'projects': [19802]}, u'attributes': []}, u'id': 260, u'value': u'Toto', u'properties': {}}

def main():
    for f in files:
        print('Scanning %s' % f)
        stats = dict()
        with open(f, 'r') as file:
            datas = json.load(file)
            values = datas["values"]
            for v in values:
                value = v["value"]
                if not value in stats.keys():
                    stats[value] = dict()
                projects = v["config"]["scope"]["projects"]
                for p in projects:
                    if not p in stats[value].keys():
                        stats[value][p] = 1
                    else:
                        stats[value][p] = stats[value][p] + 1
            for k in stats.keys():
                value = stats[k]
                for sk in value.keys():
                    sv = value[sk]
                    if sv > 1:
                        print("%s : %s : %s" % (k, sk, sv))
    return 0

main()