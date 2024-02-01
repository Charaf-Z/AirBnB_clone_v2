#!/usr/bin/python3
"""Deploy web_static content to remote servers."""

from os.path import exists, basename
from fabric.api import env, put, run

env.hosts = ["18.234.129.123", "52.3.244.13"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa_alx"


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
    file = f"/data/web_static/releases/{file_name}"
    tmp = f"/tmp/{file_name}"

    if put(archive_path, "/tmp/").failed is True:
        return False
    if run("mkdir -p {}".format(file)).failed is True:
        return False
    if run("tar -xzf {}.tgz -C {}".format(tmp, file)).failed is True:
        return False
    if run("rm -rf {}".format(tmp)).failed is True:
        return False
    if run("mv {}/web_static/* {}/".format(file, file)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s {}/ /data/web_static/current".format(file)).failed is True:
        return False
    print("New version deployed!")
    return True

