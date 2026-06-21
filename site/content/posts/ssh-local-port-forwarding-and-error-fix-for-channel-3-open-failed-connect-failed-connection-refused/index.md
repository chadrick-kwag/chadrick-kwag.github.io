---


title: 'ssh local port forwarding and error fix for "channel 3: open failed: connect
  failed: Connection refused"'
date: '2020-08-10T00:00:00+00:00'
lastmod: '2020-08-10T00:00:00+00:00'
slug: ssh-local-port-forwarding-and-error-fix-for-channel-3-open-failed-connect-failed-connection-refused
categories:
- linux
tags:
- "channel-3-open-failed"
- "ssh-local-port-forwarding"
- "ssh"
- "local"
- "port"
draft: false
---
## My Scenario

I have a remote server(4.4.4.4) where I am running a python django webserver on port 8008. However, the remove server is only allowing ssh port 32686, which means that I cannot directly access remote server at port 8008 to view the webserver. This is why I am local port forwarding through ssh so that I can access remote server port 8008 from my local host port 8355(some random port number).

## SSH command(problematic)

Looking up the guides on google, I came up with the following ssh command for my local port forwarding setup.

```generic
ssh -L 8008:4.4.4.4:8355 someuser@4.4.4.4 -p 32686
```

while ssh login worked, I cannot access the webserver from local host through port 8355. Instead, the console showed the following error.

```generic
channel 3: open failed: connect failed: Connection refused
```

## Fixed ssh command

After some more googling and internal reflection, I cam up with the correct ssh command.

```generic
ssh -L 8008:127.0.0.1:8355 someuser@4.4.4.4 -p 32686
```

When I ssh login using this command, I can now access the webserver in remote host through accessing local host port 8355.

The only difference is the remote host ip address format inside local port option definition. I think if we use the public ip of the remote host(4.4.4.4), then it will forward packets from local host to the “outside” of remote host’s port 8008 which is, as I mentioned earlier unavailable. By changing the public remote host ip address to “127.0.0.1”, I believe it is notifying remote host’s sshd that the incoming packets do not need to be redirected to the “outside” of port 8008 but rather process it internally and redirect it to the “inside” of port 8008 right away. This way it will not be blocked by the firewall.
