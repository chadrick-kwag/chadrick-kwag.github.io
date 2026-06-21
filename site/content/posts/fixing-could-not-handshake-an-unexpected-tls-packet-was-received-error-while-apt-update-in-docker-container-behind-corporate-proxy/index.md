---


title: 'fixing "Could not handshake: An unexpected TLS packet was received" error
  while apt update in docker container behind corporate proxy'
date: '2022-07-21T00:00:00+00:00'
lastmod: '2022-07-21T00:00:00+00:00'
slug: fixing-could-not-handshake-an-unexpected-tls-packet-was-received-error-while-apt-update-in-docker-container-behind-corporate-proxy
categories:
- linux
tags:
- "proxy"
- "docker"
- "apt"
- "network-error"
- "handshake"
draft: false
---
## Background

While trying to build a docker image from a very raw apache spark base image, since it didn’t have any basic packages such as vim, ssh, wget, etc, I entered a running container of this image and typed `apt update` but the following error msg was returned

```
Could not handshake: An unexpected TLS packet was received
```

This error message did not go away even though I set the `http_proxy` and `https_proxy` environment variable.

BTW, I was trying to build this docker image on a server which was behind a corporate proxy. Also when creating the container, I allowed host network access so that it can access “localhost:7007” which is a port that points to the corporate proxy.

## Solution

The solution that worked for me was from this [stackoverflow answer](https://askubuntu.com/a/1289675/297019).

I manually created a file `/etc/apt/apt.conf.d/05proxy` and added the following lines

```
Acquire::http::proxy "http://localhost:7007";
Acquire::https::proxy "http://localhost:7007";
```

where “localhost:7007” is where I have opened a port to be directed to my corporate proxy. Note that even for `https` proxy, I have forced it to point to `http` of proxy.

After adding this file and running `apt update` works.
