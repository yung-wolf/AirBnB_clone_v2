#!/usr/bin/python3

from fabric.api import task, run, put, env, local
from os.path import exists, join
from datetime import datetime

# Define the web server IP addresses
env.hosts = ['204.236.241.48', '3.90.83.137']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

@task
def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.
    """

    # Create the versions folder if it doesn't exist
    local('mkdir -p versions')

    # Generate the archive filename (web_static_<year><month><day><hour><minute><second>.tgz)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_name = f'web_static_{timestamp}.tgz'
    archive_path = join('versions', archive_name)

    # Print msg to stdout
    print(f"Packing web_static to {archive_path}")

    # Compress the contents of the web_static folder
    result = local(f'tar -cvzf {archive_path} web_static')

    if result.succeeded:
        print(f'Archive created: {archive_path}')
        return archive_path
    else:
        print('Archive creation failed.')
        return None

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
