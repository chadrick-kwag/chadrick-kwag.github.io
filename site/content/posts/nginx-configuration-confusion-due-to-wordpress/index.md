---
title: nginx configuration confusion due to wordpress
date: '2018-11-11T00:00:00+00:00'
lastmod: '2018-11-11T00:00:00+00:00'
slug: nginx-configuration-confusion-due-to-wordpress
categories:
- web
tags:
- wordpress
draft: false
---
## The problem

I practically wasted about two days because of this issue. I had no idea that wordpress could indirectly mess up with my nginx configuration.

If you are facing the following symptom when setting up wordpress with nginx, you have been in the same spot as I have.

- using a custom port(say, port 8899 in my case) to setup wordpress with nginx.
- After checking that it works with port 8899, you decide to switch it back to port 80 but also with 443 enabling SSL certificate in you system.
- After installing SSL certificate with `certbot`, you decide to change the nginx port which serves wordpress to 80 and 443.
- After changing the configuration file(either the `default` in `/etc/nginx/sites-enabled` or your own custom configuration file), you restart nginx.
- However you find that for some reason, whenever you try to access your site from outside through `http://` or `https://`, it eventually redirectly to the very first port that you used when testing wordpress functionality(which is port 8899). And since you have changed your nginx configuration to listen to only port 80 and 443, of course the redirected url(to :8899) doesn’t work.
- Weirdly, if you change the nginx configuration to listen to 8899 too, the site works but through the custom port(8899).

## What is causing it?

I dug into the nginx configurations for two days, based on my perception that url redirection stuff is all somehow done by nginx. However, it turns out that nginx configuration was not the problem.

Using `firefox`, I identified that access to port 80 and 443 was processed normally in nginx. And somehow when accessing to port 443, it was responding with a redirection to 8899.

Since I was absolutely sure that nginx configuration had nothing to do with even the keyword `8899`, it had to be whatever was after the nginx. And in this case, the culprit logically had to be wordpress. But which part of wordpress could possibly cause such redirection? Which file could possibly keep a record of the very first port(8899) number that I used to setup the wordpress?

It turns out, that wordpress did have a small place which remembered my initial configuration: the mysql database.

Checking out the mysql database that my wordpress was using, in the table `wp_options`, the first two records which are `site` and `home`, both contained the very first website url that was used when setting up wordpress. In other words, both had the value:

`http://mywordpress.com:8899`

And this url was used throughout the wordpress files so no wonder my attempt to connect through port 80 and 443 all ended up redirecting to port 8899.

After changing both record’s `option_value` field to the correct value(`https://mywordpress.com`) it worked like a charm. Now I can connect to my site without the annoying custom port tailing at my site’s url.

Please note, that even after changing this and trying to connect to your site with either `http://mywordpress.com` or `https://mywordpress.com` may display the site properly at the first connection, but while clicking through the site, the browser may erratically use the custom ported version of url. Don’t panic. this is due to the caches stored by the browser. If you delete the caches and reconnect to your site, you will not face the same problem again.
