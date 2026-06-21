---


title: 'encountering "ModuleNotFoundError: No module named ''_posixsubprocess''" error
  when running nvsysinfo'
date: '2019-05-13T00:00:00+00:00'
lastmod: '2019-05-13T00:00:00+00:00'
slug: encountering-modulenotfounderror-no-module-named-_posixsubprocess-error-when-running-nvsysinfo
categories:
- python
tags:
- "nvidia"
- "nvsysinfo"
- "modulenotfounderror"
- "false"
- "no"
draft: false
---
even confirming nvsysinfo is installed through apt, running nvsysinfo with `sudo` or even in root account produces the following error.

```generic
Original exception was:
Traceback (most recent call last):
  File "/usr/share/nvsysinfo/nvsysinfo.py", line 19, in <module>
    from nvsysinfo import collect\_nvsysinfo
  File "/usr/share/nvsysinfo/nvsysinfo/\_\_init\_\_.py", line 14, in <module>
    from collect import collect\_nvsysinfo
  File "/usr/share/nvsysinfo/nvsysinfo/collect.py", line 9, in <module>
    from subprocess import TimeoutExpired
  File "/usr/lib/python3.6/subprocess.py", line 136, in <module>
    import \_posixsubprocess
ModuleNotFoundError: No module named '\_posixsubprocess'
```

I tried reinstalling `subprocess32`module but it did not fix the problem.

However, checking out the nvsysinfo exec file which is a bash script file that practically launched a nvsysinfo.py file with python3, I manually executed it myself.

```generic
/usr/share/nvsysinfo# python3 nvsysinfo.py
Writing output to /tmp/nvsm-health-XXXXX.tar.xz

ERROR: Killing command "nc -vz -w 5 compute.nvidia.com 443" due to 10 second timeout
```

Despite the error the tar.xz file was produced in the path above. It took some time (~5min) but maybe that’s because this machine has some problems.
