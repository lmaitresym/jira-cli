# JIRA Client

*A command line client for JIRA and Confluence.*

## Purpose

This is a command line client which allows to interact with the JIRA platform.

Note: Use tag 1.1.0, tag 2.0.0 is under tests and brings a lot of untested and breaking changes.

## Installation

Preferrably in a virtualenv, install the current version::

```sh
pip install git+https://github.com/lmaitresym/jira-cli
```

## Usage

You first need to open a session in JIRA, the command you'll want to run is::

```sh
jira session login <url> <username> <api_token>
```

Before you leave, close your session::

```sh
jira session logout
```

All commands::

```sh
jira
Usage:
    jira session (login <url> <username> <password>|logout|dump)
    jira field (get <field_key_or_id_or_name>|getoptions <field_key>|addprojectoptions <field_key> <project_id>|delprojectoptions <field_key> <project_id>|loadoptions <field_key> <options_file> <project_ids>|addoptions <field_key> <options_file> <project_keys>|suggestions <field_key>|referenceDatas <field_key>|getcontext <field_key>)
    jira option (get <field_key> <option_id>|add <field_key> <option_value> <project_keys>|del <field_key> <option_id>|exist <field_key> <option_value>|replace <field_key> <option_to_replace> <option_to_use> <jql_filter>|getid <field_key> <option_value>)
    jira options add <field_key> <options_file> <project_keys>
    jira issues (get <jql> [--page=<page_index>] [--page-size=<page_size>]|getkeys <jql>|create <json_file>)
    jira issue (get <issue_key>|del <issue_key>|set <issue_keys> <field_key> <value_or_field_key>|createmeta <project_key> <issue_type>|create <json_file>)
    jira project (get <project_key_or_id>|list)
    jira role (get <project_id> <role_id>)
    jira servicedesk (get <servicedesk_id>|list)
    jira page (get <space_key> <page_title>|create <space_key> <page_title> <parent_id> [<page_file>]|delete <page_id>|update <space_key> <page_title> <page_file>|move <space_key> <page_title> <parent_id>)
    jira space (get <space_key>|list)
    jira -h | --help
    jira --version
```

Examples:

```sh
jira session login http://myhost:8080/jira myusername mypassword
jira field getoptions dsi-support-plugin__application
```

## Help

For help using this tool, please open an issue on the Github repository.

## References

- [Building Simple Command Line Interfaces in Python](https://stormpath.com/blog/building-simple-cli-interfaces-in-python)
- [JIRA Cloud REST API Reference](https://docs.atlassian.com/software/jira/docs/api/REST/1000.824.0/)
- [Confluence REST API Documentation](https://docs.atlassian.com/atlassian-confluence/REST/6.6.0/)
  - [The Confluence Cloud REST API](https://developer.atlassian.com/cloud/confluence/rest/)
  - [Confluence REST API examples](https://developer.atlassian.com/server/confluence/confluence-rest-api-examples/)
