"""
jira

Usage:
  jira session (login <url> <username> <password>|logout)
  jira field (get <field_key_or_id_or_name>|getoptions <field_key>|addprojectoptions <field_key> <project_id>|delprojectoptions <field_key> <project_id>|loadoptions <field_key> <options_file> <project_ids>|addoptions <field_key> <options_file> <project_keys>)
  jira option (get <field_key> <option_id>|add <field_key> <option_value> <project_keys>|del <field_key> <option_id>|exist <field_key> <option_value>|replace <field_key> <option_to_replace> <option_to_use> <jql_filter>|getid <field_key> <option_value>)
  jira options add <field_key> <options_file> <project_keys>
  jira issues (get <jql>|getkeys <jql>)
  jira issue (get <issue_key>|del <issue_key>|set <issue_keys> <field_key> <value_or_field_key>|createmeta <project_key> <issue_type>)
  jira project (get <project_key_or_id>)
  jira role (get <project_id> <role_id>)
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

Help:
  For help using this tool, please open an issue on the Github repository:
  http://scm.ul.mediametrie.fr/dsi-support-portal/jira-cli
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