---
title: 'error fix: pycuda "ImportError: /lib64/libstdc++.so.6: version `GLIBCXX_3.4.21''
  not found"'
date: '2021-11-19T00:00:00+00:00'
lastmod: '2021-11-19T00:00:00+00:00'
slug: error-fix-pycuda-importerror-lib64-libstdc-so-6-version-glibcxx_3-4-21-not-found
categories:
- machine-learning
tags:
- importerror
- libstdc
- pycuda
draft: false
---
## Background

I installed pycuda and was trying to run a file and error like this occured

```generic
line 62, in <module>
    from pycuda.\_driver import \*  # noqa
ImportError: /lib64/libstdc++.so.6: version \`GLIBCXX\_3.4.21' not found (required by /data/project/venv38/lib/python3.8/site-packages/pycuda-2020.1-py3.8-linux-x86\_64.egg/pycuda/\_driver.cpython-38-x86\_64-linux-gnu.so)
```

## Solution

After googling, I found [this post](https://develop-man.tistory.com/3) saying that this was due to lower version of `libstdc++.so.6`

originally my `/lib64/libstdc++.so.6` was pointing to `/lib64/libstdc++.so.6.0.19`.

But the post suggested to use a version higher. First, I needed to find if I had any versions higher than that.

```generic
$ sudo find / -name "libstdc++.so.6\*" 
```

this command will list a lot of search results. among them, I found one that had a higher version.

```generic
/var/lib/docker/overlay2/fc438c104db5df8fd007edc98975630eea749746c211d55a2838cc300a40a533/diff/usr/lib/x86\_64-linux-gnu/libstdc++.so.6
/var/lib/docker/overlay2/fc438c104db5df8fd007edc98975630eea749746c211d55a2838cc300a40a533/diff/usr/lib/x86\_64-linux-gnu/libstdc++.so.6.0.28
/var/lib/docker/overlay2/fc438c104db5df8fd007edc98975630eea749746c211d55a2838cc300a40a533/diff/usr/share/gdb/auto-load/usr/lib/x86\_64-linux-gnu/libstdc++.so.6.0.28-gdb.py
/usr/lib64/libstdc++.so.6
/usr/lib64/libstdc++.so.6.0.19
/usr/share/gdb/auto-load/usr/lib64/libstdc++.so.6.0.19-gdb.py
/usr/share/gdb/auto-load/usr/lib64/libstdc++.so.6.0.19-gdb.pyc
/usr/share/gdb/auto-load/usr/lib64/libstdc++.so.6.0.19-gdb.pyo
/usr/local/lib64/libstdc++.so.6.0.28    << this one!
/usr/local/lib64/libstdc++.so.6.0.21
/usr/local/lib64/libstdc++.so.6
/usr/local/lib64/libstdc++.so.6.0.28-gdb.py
/data/chadrick/install/gcc/gcc-9.4.0/prev-x86\_64-pc-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6.0.28
/data/chadrick/install/gcc/gcc-9.4.0/prev-x86\_64-pc-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6
/data/chadrick/install/gcc/gcc-9.4.0/stage1-x86\_64-pc-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6.0.28
/data/chadrick/install/gcc/gcc-9.4.0/stage1-x86\_64-pc-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6
```

so I changed the symbolic link to point this one

```generic
$ sudo rm /lib64/libstdc++.so.6
$ sudo ln -s /usr/local/lib64/libstdc++.so.6.0.28  /lib64/libstdc++.so.6
```

after doing this, the error did not appear.

Unfortunately I don’t know why version 6.0.28 solves this error and I was lucky enough to have a higher version lying around somewhere. If you don’t have any higher versions, I guess you will have to find a way to get one first.
