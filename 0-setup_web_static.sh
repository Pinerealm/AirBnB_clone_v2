#!/usr/bin/env bash
# Sets up a web server for the deployment of web_static files

# Install Nginx if it not already installed
sudo apt-get update
sudo apt-get install -y nginx

# Create the folder /data and its subfolders
if [ ! -d "/data/web_static/releases/test" ]; then
    sudo mkdir -p /data/web_static/releases/test
fi

if [ ! -d "/data/web_static/shared" ]; then
    sudo mkdir /data/web_static/shared
fi

# Change ownership of the /data folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Create a test HTML file in the test subfolder
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create a symbolic link to the /data/web_static/releases/test/ folder
if [ -L "/data/web_static/current" ]; then
    sudo rm /data/web_static/current
fi

ln -sf /data/web_static/releases/test /data/web_static/current

# Map the /hbnb_static/ path to the 'current' symbolic link
CONTEXT="\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;"
CONTEXT+="\n\t}\n"
FILE="/etc/nginx/sites-available/default"

if grep -q "location /hbnb_static {" $FILE; then
    echo "Context already exists"
else
    sudo sed -i --follow-symlinks "/PHP scripts to/i\ $CONTEXT" $FILE
fi

# Restart Nginx
if sudo service nginx status | grep -q "active (running)"; then
    sudo nginx -s reload
else
    sudo service nginx start
    sudo nginx -s reload
fi
