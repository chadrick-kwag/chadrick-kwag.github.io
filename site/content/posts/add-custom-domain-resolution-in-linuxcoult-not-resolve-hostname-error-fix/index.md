---
title: add custom domain resolution in linux(could not resolve hostname error fix)
date: '2020-03-23T00:00:00+00:00'
lastmod: '2020-03-23T00:00:00+00:00'
slug: add-custom-domain-resolution-in-linuxcoult-not-resolve-hostname-error-fix
categories: []
tags:
- could-not-resolve
- etc-hosts
- hostname-resolution
- linux
draft: false
---
# Problem

when the local machine is having problems resolving domain name. This can happen when using domain names that are not public but setup in corporate intranet setups.

Below is an example error message that I got when trying to git clone from corporate github which is not open to public and only accessable through intranet.

```generic
$ git clone git@somegithub.com:someuser/somereponame
Cloning into 'somereponame'…
ssh: Could not resolve hostname somegithub.com: Temporary failure in name resolution
```

# Solution

Get the ip address of the private domain name and add it to `/etc/hosts`. Below is an example

```generic
\# inside /etc/hosts

1.2.3.4 somegithub.com
```

After this, I retried the git clone and now it can communicate with `somegithub.com`.
