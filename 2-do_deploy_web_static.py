#!/usr/bin/python3
"""A Fabric script that distributes an archive to specified web servers
"""
from datetime import datetime
from fabric.api import env, put, run, local, settings
import os


env.hosts = ["100.25.167.113", "54.237.105.147"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder
    of AirBnB_clone_v2

    Returns:
        str: Path to the archive created
    """
    if not os.path.isdir("versions"):
        os.makedirs("versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date)

    print("Packing web_static to {}".format(file_name))
    with settings(warn_only=True):
        result = local("tar -cvzf {} web_static".format(file_name))
        if result.failed:
            return None
    file_size = os.stat(file_name).st_size
    print("web_static packed: {} -> {}Bytes".format(file_name, file_size))

    return file_name


def do_deploy(archive_path):
    """Distributes an archive to specified web servers

    Args:
        archive_path (str): Path to archive to be distributed

    Returns:
        bool: True if all operations were successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    file_name = archive_path.split("/")[-1]
    file_name_no_ext = file_name.split(".")[0]
    dest = "/data/web_static/releases/{}".format(file_name_no_ext)

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(dest))
        run("tar -xzf /tmp/{} -C {}/".format(file_name, dest))
        run("mv {}/web_static/* {}/".format(dest, dest))

        run("rm /tmp/{}".format(file_name))
        run("rm -rf {}/web_static".format(dest))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(dest))
    except Exception:
        return False
    else:
        print("New version deployed!")
        return True
