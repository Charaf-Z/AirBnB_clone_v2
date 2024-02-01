#!/usr/bin/env bash
# set up the server for deployement

apt-get update
apt-get -y install nginx

mkdir -p /data/web_static/releases/test /data/web_static/shared

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -hR ubuntu:ubuntu /data/

echo "server {
    listen      80 default_server;
    listen      [::]:80 default_server;

    root        /var/www/html;
    index       index.html index.htm;

    server_name _;
    add_header X-Served-By $HOSTNAME;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
