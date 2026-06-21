---


title: fix "Certificate verification failed" error in apt update of docker container
date: '2022-07-21T00:00:00+00:00'
lastmod: '2022-07-21T00:00:00+00:00'
slug: fix-certificate-verification-failed-error-in-apt-update-of-docker-container
categories:
- devops
tags:
- "docker"
- "apt"
- "tls"
- "certificates"
- "proxy"
draft: false
---
## Background

While working on a raw docker base image that didn’t even have basic tools installed, I tried to call apt update but the following error came up

```
Certificate verification failed: The certificate is NOT trusted. The certificate issuer is unknown
```

This error occurred even after setting “http_proxy” and “https_proxy” environment variables.

## Solution

This [stackoverflow answer](https://askubuntu.com/a/1375100/297019) fixed this issue.

Although it was bypass, this allowed me to avoid certificate verification during apt update.

However, after this anther error showed up. This will be discussed on [another post](/posts/fixing-could-not-handshake-an-unexpected-tls-packet-was-received-error-while-apt-update-in-docker-container-behind-corporate-proxy/).
