---


title: how to merge branch along with merge commit
date: '2020-02-28T00:00:00+00:00'
lastmod: '2020-02-28T00:00:00+00:00'
slug: how-to-merge-branch-along-with-merge-commit
categories:
- tools
tags:
- "git"
- "merge-commit"
- "merge"
- "branch"
- "along"
draft: false
---
Assume I have created a `dev` branch from `master` branch at some point. I made a few commits to `dev` and then merge these commits back to `master`. If I blatantly use the following command,

```generic
$ git checkout master
$ git merge dev
```

when checking `git log` of `master`, the commits will be added but there is no merge commit which provides some useful information on when the merge occured. This could be useful when reverting a merge since all that needs to be done is revert the merge commit.

If there wasn’t a merge commit and one had to undo the merge operation, the user will have to remove the additional commits that were applied to `master` branch which is a frusterating task to do.

If I was to merge some other branch along with a merge commit, the following command should do the trick.

```generic
$ git checkout master
$ git merge --no-ff dev
```

`--no-ff` option stands for `no fastforwarding`. This command will prompt up a confirmation of the merge commit message and after the user approves it, the `dev` commits will be merged to `master` branch along with a merge commit.
