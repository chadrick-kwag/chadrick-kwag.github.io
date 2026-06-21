---


title: add git branch indicator in bash prompt
date: '2019-04-15T00:00:00+00:00'
lastmod: '2019-04-15T00:00:00+00:00'
slug: add-git-branch-indicator-in-bash-prompt
categories:
- linux
tags:
- "git"
- "bash"
- "branch"
- "indicator"
- "prompt"
draft: false
---
# Add git branch if its present to PS1

parse_git_branch() {  
git branch 2> /dev/null | sed -e ‘/^[^*]/d’ -e ’s/* (.*)/ (\1)/'  
}

export PS1="\u@\h [\033[32m]\w[\033[33m]\$(parse_git_branch)[\033[00m] $ "
