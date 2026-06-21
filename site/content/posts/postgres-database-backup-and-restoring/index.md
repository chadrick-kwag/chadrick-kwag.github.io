---
title: postgres database backup and restoring
date: '2021-02-10T00:00:00+00:00'
lastmod: '2021-02-10T00:00:00+00:00'
slug: postgres-database-backup-and-restoring
categories:
- database
tags:
- backup
- postgres
- restore
draft: false
---
I am relatively new to postgres and at first I was backing up and restoring databases using pgadmin4. I was just using `postgres` user because this is the default one that you get to use when working with pgadmin. After developing a web project using postgres, I needed to move the database I used to somewhere else. This time, I needed to restore the backup using CLI instead of the GUI pgadmin that I was used to.

The backup sql created in pgadmin is created using custom format, which I found it hard to restore through cli commands. It failed when used with `pg_restore` for many reasons. Most of the errors that I faced was due to permissions.

Here I introduce how I created a backup of a database and restored it through cli. Other ways are possible, so just use this as a reference.

## Creating backup

For this example, I am going to backup a database named `test`. I am going to backup using `postgres` user account, which is a superuser itself. I tried backup with a created user, but it failed, so just to make things simple, I am going to backup with `postgres` account to avoid any permission issues.

I am using postgres server v13.

first change terminal user to `postgres`

```generic
$ su postgres
```

run `pg_dump` command

```generic
$ pg\_dump -d test -f dump.sql
```

Here I did not specify user since I am already `postgres` user. I am telling it to backup database named `test`, and save the dump to file named `dump.sql`.

Since `postgres` is the superuser in postgres server, this command will dump a database with least problems. This command will save sql in plain text by default.

## Restoring backup

Once this dump file has been move to a target machine, again change terminal user to `postgres`.

```generic
$ su postgres
```

use `pg_restore` to restore the database to target machine’s postgres server.

```generic
$ pg\_restore -d test < dump.sql
```

this command is telling to restore database named `test` from backup file `dump.sql`. In the dump creating command used above, it doesn’t include a sql command to create the database. Therefore, this restoring command required that a database named `test` already exists in the target machine’s postgres server. If not, then the user should create one after logging into `psql`.

For convenience, if the user want the dump file to include a database creating sql command, then the dump creating command should have `-x` option, so it should look like this:

```generic
$ pg\_dump -d test -x -f dump.sql
```

Instead of using `pg_dump` command, one can use `psql` to restore from plain sql file. The following command will read the sql commands as written with specified postgres user and database. This command also works in windows.

```generic
$ psql -U user -d dbname -f dump.sql
```

## Why change user to postgres before executing pg_dump, pg_restore?

postgres did not allow password authenticated login. It was set to peer authentication, which means that I can only login to postgres using `psql` command as `postgres` user only if I am `postgres` user in terminal. If I try to login as `postgres` user with password, it did not work. Of course, I found a workaround to force postgres server to allow `postgres` user authentication by password, but for some reason it did not work for me. Thus, the only option that I had was to change terminal user to `postgres` and then access postgres server.
