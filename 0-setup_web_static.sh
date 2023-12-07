#!/usr/bin/env bash
# Sets up web server for deployment of web_static

# install Nginx if not already installed... Nginx is already installed... start it
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi
sudo service nginx start
echo "STARTING NGINX"

# Create relevant folders
mkdir /data/
mkdir /data/web_static/
mkdir /data/web_static/releases/
mkdir /data/web_static/shared/
mkdir /data/web_static/releases/test/
echo "CREATING RELEVANT FOLDERS == SUCCESSFUL"

# Create a fake html file
echo "Hello Nginx index.html" > /data/web_static/releases/test/index.html
echo "Creating fake html file with test content (Hello Nginx index.html)"

# Create a symbolic link. Delete if it already exists
# and recreated every time the script is ran.
current_link="/data/web_static/current"
target_dir="/data/web_static/releases/test/"

if [ -L "$current_link" ]; then
    rm "$current_link"
fi

sudo ln -s "$target_dir" "$current_link"
echo "SYMBOLIC LINK CREATED: $current_link -> $target_dir"

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Backup /etc/nginx/sites-available/default
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
echo "BACKING UP NGINX CONFIG FILE"

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
# ex: https://mydomainname.tech/hbnb_static.
CONFIG="\\\tlocation /hbnb_static {\n\t\t alias /data/web_static/current/;\n\t}\n"
sed -i "30i $CONFIG" /etc/nginx/sites-available/default
echo "UPDATING NGINX CONFIG FILE"
echo "----ALL GOOD"

# Restart Nginx to reflect changes
echo "RESTARTING NGINX == SUCCESSFULLY"
sudo service nginx restart
