---


title: git error when checkout remote branch
date: '2020-02-20T00:00:00+00:00'
lastmod: '2020-02-20T00:00:00+00:00'
slug: git-error-when-checkout-remote-branch
categories:
- tools
tags:
- "git"
- "git-checkout"
- "checkout"
- "remote"
- "branch"
draft: false
---
I am currently in some branch and want to checkout to a remote branch named `dev1` which is not yet existent in local git. So I tried calling,

```generic
$ git fetch origin dev1
$ git checkout origin dev1
```

but it gave me an error.

```generic
error: pathspec 'BRANCH-NAME' did not match any file(s) known to git
```

BTW, fetching worked fine and did not complain. So I tried

```generic
$ git checkout -b dev1 origin/dev1
```

but got error:

```generic
error “Cannot update paths and switch to branch”
```

I checked if my local git was tracking remote `dev1` branch by

```generic
$ git remote show origin

remote origin
 Fetch URL: git@github.com:someuser/somegit.git
 Push  URL: git@github.com:someuser/somegit-TODAH.git
 HEAD branch: master
 Remote branch:
 dev tracked
 Local branch configured for 'git pull':
 dev merges with remote dev
 Local refs configured for 'git push':
 dev         pushes to dev         (up to date)
```

From the output, we can see local git was not tracking remote `dev1` branch.

## solution

make local git track remote `dev` branch

```generic
$ git fetch origin dev1:dev1
```

this should add tracking remote_branch_name(dev1) to local git by the name of local_branch_name(dev1). Mind the confusion due to use same name in remote and local.

now, execute

```generic
$ git checkout dev1
```

and goal is achieved.
