#!/usr/bin/python3
"""Deploy web_static content to remote servers."""
from fabric.api import env
from fabric.api import put
from fabric.api import run
from os.path import basename
from os.path import exists


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
