---


title: restart rmate when stuck
date: '2018-12-03T00:00:00+00:00'
lastmod: '2018-12-03T00:00:00+00:00'
slug: restart-rmate-when-stuck
categories:
- linux
tags:
- "rmate"
- "restart"
- "stuck"
draft: false
---
sometimes rmate setup in a remote server may not work. Causes could be numerous: simply you left it open too long and the server somehow showed erraneous behavior, or you had to abruptly shutdown your ssh connection in a forceful manner.

When the rmate is stuck, it will simply not open a file that the user commanded to open with rmate.

One way to bypass this problem is to setup a different port for rmate and use that along with `-p` option. But it really is cumbersome to keep adding this option every time you want to open a file.

So here is a tutorial on how to restart rmate.

First identify the previous rmate process that is blocking the current user’s rmate access.

```generic
$ sudo netstat -tulpn | grep 52698
```

this will show the pid that rmate is running on. Please note that without `sudo`, you won’t be able to see the pid and instead it will be displayed with `-`.

Once you have identfied the pid, then kill it. (the following example assumes that the pid has been identified as 3345)

```generic
$ sudo kill -9 3345
```

Now, you probably should be able to use `rmate` fresh and new.
