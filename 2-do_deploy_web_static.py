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

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(file))
        run("tar -xzf {} -C {}".format(tmp, file))
        run("rm -rf {}".format(tmp))
        run("mv {}/web_static/* {}/".format(file, file))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(file))
        return True
    except Exception:
        return False
