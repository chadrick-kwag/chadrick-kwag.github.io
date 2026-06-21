---
title: wget google drive large files bypassing virus check
date: '2021-06-24T00:00:00+00:00'
lastmod: '2021-06-24T00:00:00+00:00'
slug: wget-google-drive-large-files-bypassing-virus-check
categories:
- tools
tags:
- google-drive
- virus-check
- virus-ignore
- wget
draft: false
---
I was stuck with directly downloading a large google drive file(dataset file) to my server which was headless and thus I was forced to use the terminal.

However, I could not download google drive link with wget since even in a browser it cannot by pass the virus check ignore dialog.

After googling I found this [amazing post](https://www.matthuisman.nz/2019/01/download-google-drive-files-wget-curl.html) which presented a simple bash script which will handle ignoring virus check dialog and allow user to download google drive file with wget. Here is the wget script

```generic
export fileid=1sNhrr2u6n48vb5xuOe8P9pTayojQoOc\_
export filename=combian.rar

## WGET ##
wget --save-cookies cookies.txt 'https://docs.google.com/uc?export=download&id='$fileid -O- \\
     | sed -rn 's/.\*confirm=(\[0-9A-Za-z\_\]+).\*/\\1/p' > confirm.txt

wget --load-cookies cookies.txt -O $filename \\
     'https://docs.google.com/uc?export=download&id='$fileid'&confirm='$(<confirm.txt)
```

you should change the fileid and save filename appropriately. The “fileid” can be obtained from the google drive download link.

For example, for “[https://docs.google.com/uc?id=0Bz1dfcnrpXM-MUt4cHNzUEFXcmc&export=download"](https://docs.google.com/uc?id=0Bz1dfcnrpXM-MUt4cHNzUEFXcmc&export=download%22), the file id is " 0Bz1dfcnrpXM-MUt4cHNzUEFXcmc "
