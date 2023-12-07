#!/bin/bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary folders
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
sudo chown -R ubuntu:ubuntu /data

# Create a fake HTML file
echo "<html><head></head><body>HBNB Web Static Test</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"

# Add an alias to the server block
sudo sed -i '/server_name _;/a \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$nginx_config"

# Restart Nginx to apply changes
sudo service nginx restart
