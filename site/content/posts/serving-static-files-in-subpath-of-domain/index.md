---
title: serving static files in subpath of domain in django
date: '2020-04-06T00:00:00+00:00'
lastmod: '2020-04-06T00:00:00+00:00'
slug: serving-static-files-in-subpath-of-domain
categories:
- web
tags:
- django
- static-file
- subdomain
- subpath
draft: false
---
# Problem

My django project structure looks like this.(only showing files relevant to this problem)

```generic
prj/
  - prj/
    - settings.py
    - url.py
  - app/
    - urls.py
    - static/
      - js/
        - app.js
  - static/
    - js/
      - vue.js
    - css/
      - vue.css
```

As you can see, there are two static dirs that has to be served: ‘prj/app/static/`and 'prj/static`.

When serving this project from the root of a domain such as ‘localhost:8000’, the following configuration for static files in `prj/prj/settings.py` worked fine.

```python
\# prj/prj/settings.py

BASE\_DIR = os.path.dirname(os.path.dirname(os.path.abspath(\_\_file\_\_)))

STATIC\_URL = '/static/'

STATICFILES\_DIRS = \[
    os.path.join(BASE\_DIR, 'static'),
\]
```

here is the `prj/prj/url.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = \[
    path('admin/', admin.site.urls),
    path('', include("app.urls"))
```

nothing special has been done to this file.

However, this setting will not work when the django project is served from a subpath. For example, `http://localhost/somepath`. This sort of situation may arise when an nginx is running on `localhost:80`, django project running on `localhost:6000` and nginx is redirecting `http://localhost/somepath` to `localhost:6000`.

In this case, the settings above will not work even when `STATIC_URL` is changed to `/somepath/static/`. The reason is described in this [link](https://stackoverflow.com/questions/51170280/django-problems-with-static-files-when-running-in-subpath). The way I understood it, the new `STATIC_URL` will be reflected in `{% static 'js/app.js'%}` kind of tags in template html files. But it will not be reflected properly inside django’s url resolving(or ‘routing’) phase. Test it out and you will notice that the default html will be requesting for static files with proper address(e.g. `http://localhost/somepath/static/vue.js`) but it will receive a 404, meaning that the django server failed to provide the `vue.js` file.

As I said, this is due to django not able to recognize the change made in `STATIC_URL` and failing to event comprehend that it has to fetch static files.

# Solution

Since the cause is due to routing problems, the solution can be solved by manually handling the routing. There are two steps required to solve this.

## Gather all static files into one directory

First specify the `STATIC_ROOT` variable in `prj/prj/setting.py`. For this example, `gathered_static` dirname will be used.

```generic
\# prj/prj/settings.py

STATIC\_ROOT =os.path.join(BASE\_DIR, "gathered\_static")
```

then, gather all static files into one directory using the following command:

```generic
$ python manage.py collectstatic
```

this will create `gathered_static` in project root with all the static files copied. This means that `prj/app/static/js/app.js` and `prj/static/js/vue.js` `prj/static/css/vue.css` are all copied in `gathered_static/` dir. For official docs on `STATIC_ROOT`, check out this [link](https://docs.djangoproject.com/en/3.0/ref/urls/#static).

## add url pattern

Now django needs to direct all subpath to `STATIC_URL` to `gathered_static/` dir. This can be done by changing `prj/prj/urls.py` like this:

```generic
\# prj/prj/urls.py

...
from django.conf.urls.static import static
from django.conf import settings

gathered\_static\_path = os.path.join(settings.BASE\_DIR, settings.STATIC\_ROOT)

urlpatterns = \[
    path('admin/', admin.site.urls),
    path('', include("main.urls"))
\] + static('static/', document\_root=gathered\_static\_path)
```

One url pattern has been added using `static` function  
`gathered_static_path` will be pointing to the absolute path of `gathered_static`. One thing to note is that the added pattern is using `static/` and not `somepath/static`. I think this is because the `somepath` part is used up by nginx which leaves `static/` part to be passed to django server. Of course, this behavior maybe modified with a different nginx setting but this post will not covered that area.
