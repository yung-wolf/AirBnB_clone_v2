#!/usr/bin/python3

import os
from fabric.api import task, local
from datetime import datetime


@task
def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.
    """

    # Create the versions folder if it doesn't exist
    local('mkdir -p versions')

    # Generate the archive filename
    # (web_static_<year><month><day><hour><minute><second>.tgz)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_name = f'web_static_{timestamp}.tgz'
    archive_path = os.path.join('versions', archive_name)

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
