#!/usr/bin/env python
"""
This script is used to control deployment of the noogle app
"""
# Imports ######################################################################
import os
import sys

from fabric import Connection
from invoke import run

# Metadata ####################################################################
__author__ = "Timothy McFadden"
__creationDate__ = "04-JAN-2019"
__license__ = "MIT"

# Globals #####################################################################
NOOGLE_APP_HOME_FOLDER = os.environ["NOOGLE_APP_HOME_FOLDER"]
VENV_ACTIVATE = os.environ.get("NOOGLE_VENV_ACTIVATE_COMMAND", "").strip('"').strip("'")

if __name__ == "__main__":
    host = os.environ["NOOGLE_APP_HOST"]
    c = Connection(host)

    deploy_commands = [
        "pip install -e .[dev]",
        "pip install -r requirements.txt",
        "noogle dev build",
    ]

    with c.cd(NOOGLE_APP_HOME_FOLDER):
        c.run("git fetch")
        c.run("git reset --hard origin/master")

        if VENV_ACTIVATE:
            with c.prefix(VENV_ACTIVATE):
                for command in deploy_commands:
                    c.run(command, hide='stdout')
                c.run("sudo bash _build/deploy.bash", pty=True)
        else:
            for command in deploy_commands:
                c.run(command, hide='stdout')
            c.run("sudo bash _build/deploy.bash", pty=True)