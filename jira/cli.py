"""
jira

Usage:
  jira session (login <url> <username> <password>|dump)
  jira field (getall|get <field_key_or_id_or_name>|getoptions <field_key> <context>|addprojectoptions <field_key> <project_id>|delprojectoptions <field_key> <project_id>|loadoptions <field_key> <options_file> <project_ids>|addoptions <field_key> <options_file> <project_keys>|suggestions <field_key>|referenceDatas <field_key>|getcontexts <field_key>|create <name> <description> <searcher_key> <field_type>|getbyid <custom_field_id>|getbyname <field_name>|trash <field_id>|restore <field_id>|delete <field_id>|delcontext <field_id> <context_id>|addoption <field_key> <context_id> <option_value>|deloption <field_key> <context_id> <option_id>|delalloptions <field_key> <context_id>)
  jira option (get <field_key> <option_id>|add <field_key> <option_value> <project_keys>|del <field_key> <option_id>|exist <field_key> <option_value>|replace <field_key> <option_to_replace> <option_to_use> <jql_filter>|getid <field_key> <option_value>|addcascading <field_key> <context_id> <parent_id> <option_value>|delcascading <field_key> <context_id> <parent_id> <option_id>)
  jira options add <field_key> <options_file> <project_keys>
  jira issues (get <jql> [--page=<page_index>] [--page-size=<page_size>] [--fields=<field1,field2...>]|getkeys <jql>|create <json_file>)
  jira issue (get <issue_key> [--fields=<field1,field2...>]|del <issue_key>|set <issue_keys> <field_key> <value_or_field_key>|createmeta <project_key> <issue_type>|create <json_file>)
  jira issuetype (get <issuetype_key>|getall|getbyproject <project_id>)
  jira project (get <project_key_or_id>|list)
  jira role (get <project_id> <role_id>)
  jira servicedesk (get <servicedesk_id>|list)
  jira page (get <space_key> <page_title>|create <space_key> <page_title> <parent_id> [<page_file>]|delete <page_id>|update <space_key> <page_title> <page_file>|move <space_key> <page_title> <parent_id>)
  jira screen (get <screen_id>|gettabs <screen_id> <project_id>|addFieldToTab <screen_id> <tab_id> <field_id>)
  jira server (infos)
  jira space (get <space_key>|list)
  jira task (get <task_id>|cancel <task_id>)
  jira settings (get <setting_key>|list [<category>]|set <setting_key> <setting_value>)
  jira -h | --help
  jira --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  jira session login https://myhost.atlassian.net myusername mypassword
  jira field
  jira field getoptions dsi-support-plugin__application
  jira option del dsi-support-plugin__application 1
  jira option del dsi-support-plugin__application 1..28
  jira option replace dsi-support-plugin__application 1 52 "*"
  jira issue get DSP-10
  jira issue set DSP-15..DSP-57 description *dsi-support-plugin__description
  jira issue set DSP-15..DSP-57 description "New description"
  jira issue set DSP-10 description *dsi-support-plugin__description
  jira option exist dsi-support-plugin__application "toto"
  jira options add dsi-support-plugin__application ../only_produits.csv 20211,19802
  jira field loadoptions dsi-support-plugin__typeIncident options_to_restore.json 20211,19802
  jira project get PID
  jira role get 18090 10080 | jq '.actors[] | .displayName'
  jira space get SCRUM

Help:
  For help using this tool, please open an issue on the Github repository.
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

import json
import inspect


def main():
    """Main CLI entrypoint."""
    import jira.commands
    options = docopt(__doc__, version=VERSION)

    #print("In entry point: %s" % json.dumps(options,indent=2))
    #print("Commands: %s" % json.dumps(dir(jira.commands),indent=2))

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        #print("Look for %s (and %s)" % (k, v))
        if hasattr(jira.commands, k) and v:
            module = getattr(jira.commands, k)
            jira.commands = getmembers(module, isclass)
            command = [command[1] for command in jira.commands if command[0] != 'Base' and inspect.getmodule(
                command[1]).__name__.startswith('jira.commands')][0]
            #print("Command is %s" % command.__name__)
            command = command(options)
            command.run()
