---
title: fixing intellij remote password not properly saved error
date: '2020-07-09T00:00:00+00:00'
lastmod: '2020-07-09T00:00:00+00:00'
slug: fixing-intellij-remote-password-not-properly-saved-error
categories: []
tags:
- intellij-password
draft: false
---
## Problem

After windows update, for some reason I have to keep re-entering remote server passwords whenever I start intelliJ and work on a remote server. This did not happen before. Before this problem happened, I only need to enter the password once, save it, and it would not ask the password ever again. It automatically accessed the remote server smoothly.

## Solution

Go to `Settings-Appearance & Behavior - System Settings - Passwords`

Check `In KeePass`

Click `Clear` after clicking the gear icon button.

After doing this, I entered remote server passwords once and it did not ask again.
