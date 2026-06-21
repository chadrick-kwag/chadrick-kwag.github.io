---


title: allowing remote access to mysql db from anywhere
date: '2019-05-02T00:00:00+00:00'
lastmod: '2019-05-02T00:00:00+00:00'
slug: allowing-remote-access-to-mysql-db-from-anywhere
categories:
- database
tags:
- "remote-access"
- "mysql"
- "remote"
- "access"
- "db"
draft: false
---
## Change mysqld configuration

Locate the mysql server configuration file. For me, it was under `/etc/mysql/mysql.conf.d/mysqld.cnf`

```generic
\[mysqld\]
#
# \* Basic Settings
#
user		= mysql
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
port		= 3306
basedir		= /usr
datadir		= /var/lib/mysql
tmpdir		= /tmp
lc-messages-dir	= /usr/share/mysql
skip-external-locking
#
# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
#bind-address		= 127.0.0.1
#
# \* Fine Tuning
#
```

As you can see above, comment out the `bind-address` option. This will allow access to mysql port from anywhere.

## Grant privilege to user coming from remote host

If the user created a mysql account following the basic tutorials out there, it is likely that the account was created only to allow access from localhost. This will block access to database using the mysql user account even though the mysql server port is available from external hosts. in order to allow user account access from anywhere, the user will need to grant the target user account from external hosts with adequate privileges as well.

Once entering mysql console with root, do the following:

```generic
grant all on <database\_name>.\* to 'username'@'%' identified by 'user\_password';
```
