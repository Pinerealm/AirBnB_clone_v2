#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents of
AirBnB_clone_v2 web_static folder
"""
from fabric.api import local, settings


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder
    of AirBnB_clone_v2
    """
    try:
        with settings(warn_only=True):
            if local("test -d versions").failed:
                local("mkdir versions")
        date = local("date +%Y%m%d%H%M%S", capture=True)
        file_name = local('echo "versions/web_static_{}.tgz"'
                          .format(date), capture=True)
        local("tar -cvzf {} web_static".format(file_name))

        return file_name
    except Exception:
        return None
