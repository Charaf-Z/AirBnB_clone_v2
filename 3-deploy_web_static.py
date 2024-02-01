#!/usr/bin/python3
"""Automated deployment script for web_static content."""
from fabric.api import *
from datetime import datetime
from os.path import exists
from os.path import basename


env.hosts = ["18.234.129.123", "52.3.244.13"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa_alx"


def do_pack():
    """
    Create a compressed archive of the web_static folder.

    Returns:
        str: The file path of the created archive,
            or None if the process fails.
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None


def do_deploy(archive_path):
    """
    Deploy the web_static content to remote servers.

    Args:
        archive_path (str): Path to the compressed archive to deploy.

    Returns:
        bool: True if deployment succeeds, False otherwise.

    Raises:
        Exception: If an error occurs during the deployment process.
    """
    if exists(archive_path) is False:
        return False
    file_name = basename(archive_path).split(".")[0]
    file = "/data/web_static/releases/{}/".format(file_name)
    tmp = "/tmp/{}.tgz".format(file_name)
    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(file))
        run("tar -xzf {} -C {}".format(tmp, file))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(file, file))
        run("rm -rf {}/web_static".format(file))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(file))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Automate the process of creating and deploying web_static content.

    Returns:
        bool: True if the deployment process succeeds, False otherwise.
    """
    file_path = do_pack()
    if exists(file_path) is False:
        return False
    rsl = do_deploy(file_path)
    return rsl
