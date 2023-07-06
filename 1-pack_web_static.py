#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents of
AirBnB_clone_v2 web_static folder
"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder
    of AirBnB_clone_v2
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))

        return file_name
    except Exception:
        return None
