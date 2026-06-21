---
title: bash script for checking rmate port is available or not
date: '2019-05-03T00:00:00+00:00'
lastmod: '2019-05-03T00:00:00+00:00'
slug: bash-script-for-checking-rmate-port-is-available-or-not
categories:
- linux
tags:
- bash
- port
- rmate
draft: false
---
```generic
portnum=52698
result=$(echo <sudopassword> | sudo -S netstat -tulpn | grep $portnum | wc -l)
echo "\\n"
if \[ $result -eq 0 \]
then
    echo -e "\\e\[31m$portnum not available\\e\[0m"
else
    echo -e "\\e\[32m$portnum available\\e\[0m"
fi


```
