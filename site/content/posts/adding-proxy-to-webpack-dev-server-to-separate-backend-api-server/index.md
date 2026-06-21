---
title: adding proxy to webpack dev server to separate backend api server
date: '2020-03-04T00:00:00+00:00'
lastmod: '2020-03-04T00:00:00+00:00'
slug: adding-proxy-to-webpack-dev-server-to-separate-backend-api-server
categories: []
tags:
- webpack-dev-server
- webpack-dev-server-data-api
- webpack-dev-server-proxy
- webpack-dev-server-react
draft: false
---
webpack-dev-server is a wonderful tool when developing due to live reloading features when working on react projects. However, a complication arises when the user begins to add data serving apis.

By default, webpack-dev-server only serves the front-end related files when started, which leaves no room for the user to squash in data serving code initialization during startup. For example, I want to fetch some data from the server. One option would be to setup a data serving api server in a different domain, but this option causes CORS which adds frustration and it isn’t neat. If I want to have the data serving api to have the same domain as the front-end serving domain, AND do not surrender using webpack-dev-server, the following solution will solve the dilemma.

# Solution

webpack-dev-server has `proxy` configuration where it allows proxying certain subdomain paths to some other domain. For example, I have setup a data serving api on `localhost:3000` where the data can be fetched when GETing `http://localhost:3000/api`. The webpack-dev-server is running on port 8080, so my dev react project is live on `http://localhost:8080`. Somewhere in my react code, I want to fetch data by sending GET request to `localhost:3000/api` but this will raise CORS error.

But what if webpack-dev-server can forward requests to `http://localhost:8080/api` to `http://localhost:3000/api`? This is what `proxy` configuration does.

For this example’s purpose, adding following configuration in `webpack.config.js` will do.

```generic
    devServer: {

    // use port 8080
    // other options...

        proxy: {
            '/api': 'http://localhost:3000'
        }

    }
```

restart the webpack-dev-server and any requests to `localhost:8080/api` will be automatically forwarded to `localhost:3000/api`.

More specific options are available for `proxy` options, such as path modification before forwarding. Checkout the [docs](https://webpack.js.org/configuration/dev-server/#devserverproxy).

This way, the browser does not need to raise CORS error and the user can separate front-end serving and backend data serving in different node processes. This will allow the user to enjoy the webpack-dev-server’s live reloading feature and modify data serving server when required.
