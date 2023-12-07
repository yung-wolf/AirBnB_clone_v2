#!/usr/bin/python3

from fabric.api import task, run, put, env
from os.path import exists

# Define the web server IP addresses
env.hosts = ['204.236.241.48', '3.90.83.137']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


@task
def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    """
    # Checks if archive exists
    if not exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return False

    # Extract the filename without extension from the archive path
    archive_filename = archive_path.split("/")[-1].split(".")[0]

    # Upload the archive to the /tmp/ directory on the web servers
    put(local_path=archive_path, remote_path='/tmp/')

    # Uncompress the archive to /data/web_static/releases/<archive filename
    # without extension>
    full_folder = f'/data/web_static/releases/{archive_filename}'
    run(f'mkdir -p {full_folder}')
    run(f'tar -xzf /tmp/{archive_filename}.tgz -C {full_folder}')

    # Delete the archive from the web server
    run(f'rm /tmp/{archive_filename}.tgz')

    # Rename achive file and remove dir of previous name
    run(f"mv {full_folder}/web_static/* {full_folder}")
    run(f"rm -rf {full_folder}/web_static")

    # Delete the symbolic link /data/web_static/current
    current_link = '/data/web_static/current'
    run(f'rm -rf {current_link}')

    # Create a new symbolic link /data/web_static/current linked to the new
    # version
    run(f'ln -s {full_folder} {current_link}')

    print("New version deployed!")
    return True
