#!/usr/bin/python3
"""Deploy web_static content to remote servers."""
from datetime import datetime
from fabric.api import env
from fabric.api import put
from fabric.api import run
from fabric.api import local
from os.path import isfile, basename


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
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date)
    if isfile(file_name):
        return file_name
    if isdir("version") is False:
        if local("mkdir -p versions").failed is False:
            return None
    if local("tar -cvzf {} web_static".format(file_name)).failed is True:
        return None
    print("Packing web_static to {}")
    return file_name


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
    if isfile(archive_path) is False:
        return False
    file_name = basename(archive_path).split(".")[0]
    file = f"/data/web_static/releases/{file_name}/"
    tmp = f"/tmp/{file_name}.tgz"

    try:
        if put(archive_path, "/tmp/").failed is True:
            return False
        if run("rm -rf {}".format(file)).failed is True:
            return False
        if run("mkdir -p {}".format(file)).failed is True:
            return False
        if run("tar -xzf {} -C {}".format(tmp, file)).failed is True:
            return False
        if run("rm {}".format(tmp)).failed is True:
            return False
        if run("mv {}/web_static/* {}/".format(file, file)).failed is True:
            return False
        if run("rm -rf {}/web_static".format(file)).failed is True:
            return False
        if run("rm -rf /data/web_static/current").failed is True:
            return False
        if (
            run("ln -s {} /data/web_static/current".format(file)).failed
            is True
        ):
            return False
        print("New version deployed!")
        return True
    except Exception:
        return False
