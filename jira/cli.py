"""
jira

Usage:
  jira session [login <url> <username> <password>|logout]
  jira field [getoptions <field_key>|addprojectoptions <field_key> <project_id>|delprojectoptions <field_key> <project_id>]
  jira option [get <field_key> <option_id>|add <field_key> <option_value>|del <field_key> <option_id>]
  jira issue [get <issue_key>|del <issue_key>|set <issue_keys> <field_key> <value_or_field_key>|createmeta <project_key> <issue_type>]
  jira -h | --help
  jira --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  jira session login https://myhost.atlassian.net myusername mypassword
  jira field
  jira field getoptions <field_key>
  jira issue get DSP-10
  jira issue set DSP-15..DSP-57 description *dsi-support-plugin__description
  jira issue set DSP-15..DSP-57 description "New description"
  jira issue set DSP-10 description *dsi-support-plugin__description

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rastaman/jira-cli
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

import inspect


def main():
    """Main CLI entrypoint."""
    import jira.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():

        if hasattr(jira.commands, k) and v:
            module = getattr(jira.commands, k)
            jira.commands = getmembers(module, isclass)
            command = [command[1] for command in jira.commands if command[0] != 'Base' and inspect.getmodule(
                command[1]).__name__.startswith('jira.commands')][0]
            command = command(options)
            command.run()
