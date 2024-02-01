#!/usr/bin/python3
"""Automated deployment script for web_static content."""
from fabric.api import *
from datetime import datetime
from os.path import exists
from os.path import basename
from os.path import getsize


env.hosts = ["18.234.129.123", "52.3.244.13"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa_alx"
created_archive = None


def do_pack():
    """
    Create a compressed archive of the web_static folder.

    Returns:
        str: The file path of the created archive,
            or None if the process fails.
    """
    global created_archive
    if created_archive is not None:
        return created_archive
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date)
    print(f"Packing web_static to {file_name}")
    try:
        if not exists('versions'):
            local("sudo mkdir -p versions")
        local("sudo tar -cvzf {} web_static".format(file_name))
        print(f"Packing web_static to: {file_name} -> {getsize(file_name)}")
        created_archive = file_name
        return file_name
    except Exception:
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
        run("mv {}web_static/* {}".format(file, file))
        run("rm -rf {}web_static".format(file))
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
    if not exists(file_path):
        return False
    rsl = do_deploy(file_path)
    return rsl
