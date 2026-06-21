---


title: git lfs smudge error fix
date: '2020-01-09T00:00:00+00:00'
lastmod: '2020-01-09T00:00:00+00:00'
slug: git-lfs-smudge-error-fix
categories:
- linux
tags:
- "git-lfs"
- "proxy"
- "smudge-error"
- "git"
- "lfs"
draft: false
---
this is a solution for a specific case. The environment is under a corporate setting where firewalls are in place.

- server1: github server
- server2: development server. the place where I want to clone a repo.
- server3. another development server. cloning/push/pulling from the repo works without errors.

While I was working on server3, git lfs worked flawlessly.  
However, when I was trying to clone/pull from server2, the procedure always failed due to an error.

Using a verbose command, I was able to get a more detailed look at logs related to the cause of failure.

To get a more verbose command add `GIT_CURL_VERBOSE=1 GIT_TRACE=1` in front of the command like the following.

```generic
$ GIT\_CURL\_VERBOSE=1 GIT\_TRACE=1 git clone <repo-url> <save\_dir\_name>
```

The cause was that from server2, it was unable to reach server1 github’s git lfs url.

First this seemed weird because non lfs git objects were downloaded/updated successfully which means that communication between server2 and server1 was fine when it came to normal git objects.

Then I found the cause. There was a `http.proxy` `https.proxy` git config set globally.

Since git lfs only works though https, when dealing with git lfs objects it tryied to access the git lfs url on server1 through the https.proxy.  
The non lfs git objects were updated through ssh and not http/https, thus was not using any kind of proxy.

I removed the `http.proxy` and `https.proxy` config in my repo by

```generic
$ git config http.proxy ""
$ git config https.proxy ""
```

and after this, git lfs downloading worked just like the non lfs objects did.
