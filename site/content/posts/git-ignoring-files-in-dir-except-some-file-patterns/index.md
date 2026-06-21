---
title: git ignoring files in dir except some file patterns
date: '2020-03-31T00:00:00+00:00'
lastmod: '2020-03-31T00:00:00+00:00'
slug: git-ignoring-files-in-dir-except-some-file-patterns
categories:
- tools
tags:
- git-ignore
draft: false
---
# Problem

In cases of config dirs, I want to add a sample config file to git but ignore non-sample files that is actually used in local. For example,

```generic
\- src/
  - config/
    - config.sample.json
    - using\_config.json
```

I am using `using_config.json` but do not want this to be added to git. On the other hand I do want `config.sample.json` to be added and tracked by git.  
Of course, this can be done by adding `.gitignore` under `src/config` but if I have multiple config dirs across my project, it is cumbersome to add `.gitignore` to every config file.

# Solution

Controlling gitignore in all config dirs can be done by the `.gitignore` file in project root.

```generic
\*\*/config/\*
!\*\*/config/\*.sample.json
```

adding these two lines to the root `.gitignore` will track only `*.sample.json` pattern files in `config` dirs and ignore all others.

Note, if `**/config` was used instead of `**/config/*`, then the gitginore will not behave as I intended. The trailing `/*` is significant.
