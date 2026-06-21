---
title: '"X11 proxy: Unsupported authorisation protocol" error fix'
date: '2020-03-05T00:00:00+00:00'
lastmod: '2020-03-05T00:00:00+00:00'
slug: x11-proxy-unsupported-authorisation-protocol-error-fix
categories: []
tags:
- nautilus-error
- unsupported-authorisation-protocol
- x11-forwarding
- xauthority
draft: false
---
when calling nautlius on a remote server, I got the following error message.

```generic
$ nautilus
MoTTY X11 proxy: Unsupported authorisation protocol
Failed to connect to Mir: Failed to connect to server socket: No such file or directory
Unable to init server: Could not connect: Connection refused
```

I was using MobaXterm, with X11 forwarding option on.

# Cause & Solution

For my case, this was due to `.Xauthority` file lock down. from my home directory(`/home/user`), here is the `ls` output

```generic
.Xauthority
.Xauthority-c
.Xauthority-l
```

from googling, the “-c” and “-l” suffix files are lock files for `.Xauthority`. So I simply deleted those two files.

Also, I’m not sure if this is critical, I changed the ownership of `.Xauthority` from root to current user. I haven’t tested if this is the critical factor of solving the issue, but I think removing the lock files is the more critical one. Writing it down, just in case.

After deleteing the lock files, close your session and reconnect. Then call `nautilus`. It should work.

# facing other troubles

Even after deleting the lock files, and executing `nautilus`, you may get the following error:

```generic
$ nautilus .
MoTTY X11 proxy: unable to connect to forwarded X server: Network error: Connection refused
Failed to connect to Mir: Failed to connect to server socket: No such file or directory
Unable to init server: Could not connect: Connection refused

(nautilus:31040): Gtk-WARNING \*\*: cannot open display: localhost:10.0
```

this is because you haven’t closed the session and reopened it. the old session, which failed to setup x11 forwarding properly from the very start. That’s why you should reopen the session so that proper x11 forwarding initialization is taken place.
