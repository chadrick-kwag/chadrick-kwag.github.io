---


title: gitignore ignore config files except sample config file
date: '2021-02-16T00:00:00+00:00'
lastmod: '2021-02-16T00:00:00+00:00'
slug: gitignore-ignore-config-files-except-sample-config-file
categories:
- linux
tags:
- "git"
- "gitignore"
- "sample-files"
- "ignore"
- "files"
draft: false
---
I usually keep my configuration files under a directory named `config` but I don’t want these config files to be tracked by git. However, I do place a sample configuration file which I wish to be tracked by git. Normally, I name these sample configuration files as `config.sample.yaml` or `config.sample.yaml`. If there is only one `config` directory that I work, then this problem can be easily solved by placing another `.gitignore` file inside `config` dir, but I have multiple `config` dirs across my project and adding `.gitignore` in each of those directories and managing them seems like a really irritating way to do it.

I can achieve what I want by configuring `.gitignore` in the root of my project directory like this.

```generic
\*\*/config/\*\*/\*.yaml
\*\*/config/\*\*/\*.json
!\*\*/config/\*\*/\*.sample.yaml
!\*\*/config/\*\*/\*.sample.json
```
