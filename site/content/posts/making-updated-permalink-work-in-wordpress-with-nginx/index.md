---


title: making updated permalink work in wordpress with nginx
date: '2019-05-07T00:00:00+00:00'
lastmod: '2019-05-07T00:00:00+00:00'
slug: making-updated-permalink-work-in-wordpress-with-nginx
categories:
- web
tags:
- "wordpress"
- "nginx"
- "not-working"
- "permalink"
- "updated"
draft: false
---
After I changed my permalink type to use postname and applied the changes, accessing posts gave me a 404 while the wordpress site was running perfectly fine.

The problem was due to the fact that I was using nginx. If I was using apache, I would have had the changes in the permalinks dealt with automatically with a high chance. However if nginx was used, then some manual fix needed to be done.

The fix is simple, just replace one line to another in the nginx configuration file for your wordpress website under `/etc/nginx/sites-enabled`

After changing it, it looks like this:

```generic
        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.

                try\_files $uri $uri/ /index.php?$args;
                # try\_files $uri $uri/ =404;
                index index.php;
        }

```

So I commented out the `try_files $uri $uri/ =404;` and replaced it with the `try_files $uri $uri/ /index.php?$args;` line. This fix was from [here](https://www.cyberciti.biz/faq/how-to-configure-nginx-for-wordpress-permalinks/).

What this fix does is, when an request is made, the nginx will catch it and attempt to process it by simply adding `/` at the end. The original line would throw 404 when it fails to find any proper way to handle it.

However, the new line will try processing it by adding `/index.php?args` suffixed to the incoming request. This way, the request will be further processed through `index.php` which seems to be the core of wordpress. I guess the new permalinks is now handled safely with `index.php` and thus fixing my problem.
