---


title: qtwindeploy output missing 'libgcc_s_seh-1.dll' error fix
date: '2021-09-19T00:00:00+00:00'
lastmod: '2021-09-19T00:00:00+00:00'
slug: qtwindeploy-output-missing-libgcc_s_seh-1-dll-error-fix
categories:
- tools
tags:
- "libgcc-s-seh-1-dll"
- "qt"
- "windeployqt"
- "qtwindeploy"
- "output"
draft: false
---
While deploying qt in windows, the official docs recommend using `windeployqt.exe`

However, once the outputs of windeployqt.exe are packaged and executed in a different machine without any qt installments, I encountered “msising libgcc_s_seh-1.dll” error.

# Solution

When I ran windeployqt.exe, I just ran it from powershell.

When I used the Qt 5.12.6(MinGW 7.3 64-bit) terminal, and executed windeployqt.exe the same way as I did before, the outputs were different, and this time it had copied “libgcc_s_seh-1.dll” to the output directory.

After packaging this output and running in a different machine, the executable ran okay without errors.

So the solution is to run windeployqt.exe from the QT’s mingw terminal that is installed in your computer.
