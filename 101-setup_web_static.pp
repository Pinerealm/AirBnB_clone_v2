# Set up a web server for deployment of the web_static folder

# 1. Update the apt package index
exec { 'apt-get update':
  command => 'apt-get update',
  path    => '/usr/bin',
}

# 2. Ensure that nginx is installed
package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt-get update'],
}

# 3. Create the folder /data and its subfolders
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# 4. Create Create a test HTML file in the test subfolder
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content =>
  '<html>
    <head>
    </head>
    <body>
      Holberton School
    </body>
  </html>',
}

# 5. Create a symbolic link to the /data/web_static/releases/test/ folder
exec { 'ln -sf /data/web_static/releases/test/ /data/web_static/current':
  path    => '/usr/bin',
  creates => '/data/web_static/current',
}

# 6. Give ownership of the /data/ folder to the ubuntu user AND group
exec { 'chown -R ubuntu:ubuntu /data/':
  path    => '/usr/bin',
}

# 7. Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content =>
  "server {
          listen 80 default_server;
          listen [::]:80 default_server;

          root /var/www/html;

          # Add index.php to the list if you are using PHP
          index index.html index.htm index.nginx-debian.html;

          server_name _;

          location / {
                  # First attempt to serve request as file, then
                  # as directory, then fall back to displaying a 404.
                  try_files \$uri \$uri/ =404;
          }
    
          location /redirect_me {
                  return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
          }

          error_page 404 /custom_404.html;
          location = /custom_404.html {
                  root /usr/share/nginx/html;
                  internal;
          }

          location /hbnb_static {
                  alias /data/web_static/current/;
          }
  }",
  notify  => Service['nginx'],
}

# 8. Restart nginx
service { 'nginx':
  ensure     => 'running',
  enable     => 'true',
  hasrestart => 'true',
  require    => File['/etc/nginx/sites-available/default'],
}
