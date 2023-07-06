#!/usr/bin/python3
"""A Fabric script that deletes out-of-date archives
"""
from fabric.api import env, run, local
from datetime import datetime
import os


env.hosts = ["100.25.167.113", "54.237.105.147"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_clean(number=0):
    """Deletes out-of-date archives
    """
    number = int(number)
    if number in (0, 1):
        number = 1

    local("ls -d -1tr versions/* | head -n -{} | \
          xargs -d '\n' rm -f --".format(number))

    run("ls -d -1tr /data/web_static/releases/* | head -n -{} | \
        xargs -d '\n' rm -rf --".format(number))
