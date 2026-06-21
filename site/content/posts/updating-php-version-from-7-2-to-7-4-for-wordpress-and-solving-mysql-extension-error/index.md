---
title: updating php version from 7.2 to 7.4 for wordpress and solving mysql extension
  error
date: '2021-06-28T00:00:00+00:00'
lastmod: '2021-06-28T00:00:00+00:00'
slug: updating-php-version-from-7-2-to-7-4-for-wordpress-and-solving-mysql-extension-error
categories: []
tags:
- error
- mysql-extension
- php-7-4
- php-version-update
- wordpress
draft: false
---
I am running my wordpress in aws and recently my wordpress dashboard was giving my warnings to update php version from 7.2 to 7.4 for security.

# Updating php version

I am currently using Ubuntu 18.04 version. This Ubuntu version doesn’t natively support php 7.4. So the following commands were required to install php7.4

```generic
$ sudo add-apt-repository ppa:ondrej/php
$ sudo apt update
$ sudo apt install php7.4
```

check php version with the following command

```generic
$ php --version
PHP 7.4.20 (cli) (built: Jun  4 2021 21:24:37) ( NTS )
Copyright (c) The PHP Group
Zend Engine v3.4.0, Copyright (c) Zend Technologies
    with Zend OPcache v7.4.20, Copyright (c), by Zend Technologies
```

# Install php7.4-fpm

installing php7.4 isn’t enough for wordpress running with nginx to recognitze the new version of php. I need to install `php7.4-fpm` so that nginx will use php7.4

```generic
$ sudo apt install php7.4-fpm
```

After installing this package, I need to modify my nginx configuration for wordpress site to use this new fpm.

I modified `/etc/nginx/sites-enabled/my-site-configuration-file` file. This file has the following part

```generic
 # pass PHP scripts to FastCGI server
        #
        location ~ \\.php$ {
                #include snippets/fastcgi-php.conf;

                # With php-fpm (or other unix sockets):
                fastcgi\_pass unix:/var/run/php/php7.2-fpm.sock; #<<< change here!!

                include         fastcgi\_params;
                fastcgi\_param   SCRIPT\_FILENAME    $document\_root$fastcgi\_script\_name;
                fastcgi\_param   SCRIPT\_NAME        $fastcgi\_script\_name;
```

In there, I change the line configuration fpm by changing “php7.2-fpm.sock” -> “php7.4-fpm.sock”

After modifying the nginx configuration file, we need to restart nginx.

```generic
$ sudo service nginx restart
```

# “Your PHP installation appears to be missing the MySQL extension which Is required by WordPress” error

However, restarting nginx shows the “Your PHP installation appears to be missing the MySQL extension which Is required by WordPress” error. This can be solved by installing a mysql extension for php 7.4

```generic
$ sudo apt install php7.4-mysql
```

with this package installed, the wordpress will now run well with php7.4
