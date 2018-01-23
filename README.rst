jira-cli
========

*A command line client for JIRA.*


Purpose
-------

This is a command line client which allows to interact with the JIRA platform.

Usage
-----

You first need to open a session in JIRA, the command you'll want to run is::

    $ jira session login <url> <username> <password>

Before you leave, close your session::

    $ jira session logout

All commands::

```sh
  jira session [login <url> <username> <password>|logout|get]
  jira -h | --help
jira --version
``````````````

Examples::

    $ jira session login http://myhost:8080/jira myusername mypassword
    $ jira system tenant pause

Help
----

For help using this tool, please open an issue on the Github repository:
https://scm.ul.mediametrie.fr/dsi-support-portal/jira-cli

References
----------

 * `Building Simple Command Line Interfaces in Python <https://stormpath.com/blog/building-simple-cli-interfaces-in-python>`__
