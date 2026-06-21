---
title: webpack dev server live reloading not working fix
date: '2020-03-01T00:00:00+00:00'
lastmod: '2020-03-01T00:00:00+00:00'
slug: webpack-dev-server-live-reloading-not-working-fix
categories: []
tags:
- hot-reload
- webpack-dev-server-hot-reload
- webpack-dev-server-not-working
draft: false
---
There are numerous solutions out there on google, but none seemed to work. [This post](https://medium.com/code-oil/burning-questions-with-answers-to-why-webpack-dev-server-live-reload-does-not-work-6d6390277920) greatly helped me understand differences among confusing concepts such as `publicPath`, `live reload`, `hot module replacement(HMR)`, `watchContentBase`, etc. However even this informative post didn’t solve my simple react + webpack setup. I think the informative post is worth looking into but small modifications to its explanations must be made.

## Problematic Setup

Here’s my initial setup, where I’m running a very simple react example.

```generic
.
├── package.json
├── node\_modules
├── package-lock.json
├── README.md
├── src
│   ├── index.html
│   ├── index.js
│   └── vis.js
└── webpack.config.js
```

The main entry is `src/index.js` which imports `src/vis.js`.

Here’s my original `webpack.config.js`

```generic
var path = require('path');
var HtmlWebpackPlugin =  require('html-webpack-plugin');

module.exports = {
    entry : './src/index.js',
    output : {
        path : path.resolve(\_\_dirname , 'dist'),
        filename: 'index\_bundle.js'
        
    },
    module : {
        rules : \[
            {test : /\\.(js)x?$/, use:\['babel-loader'\]},
            {test : /\\.css$/, use:\['style-loader', 'css-loader'\]}
            
        \]
    },
    mode:'development',
    plugins : \[
        new HtmlWebpackPlugin ({
            template : 'src/index.html',
            
        })
    \],

    devServer: {
        open: true,
        // tried my configs here...
        
    }

}
```

Where I’ve tried various different configs in `devServer` section such as…

```generic
// inside devServer section
{
    open: true,
    publicPath: "/dist/"
}
```

```generic
{
    open: true,
    watchContentBase: true
}
```

btw the above config gives an error:

```generic
\> my-app@0.1.0 dev-start /home/prj/webprjs/my-app
> webpack-dev-server

events.js:167
      throw er; // Unhandled 'error' event
      ^

Error: ENOSPC: no space left on device, watch '/home/chadrick/prj/web/timeline\_test/my-app'
    at FSWatcher.start (internal/fs/watchers.js:164:26)
    at Object.watch (fs.js:1232:11)
    at createFsWatchInstance (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:38:15)
    at setFsWatchListener (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:81:15)
    at FSWatcher.NodeFsHandler.\_watchWithNodeFs (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:233:14)
    at FSWatcher.NodeFsHandler.\_handleDir (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:429:19)
    at FSWatcher.<anonymous> (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:477:19)
    at FSWatcher.<anonymous> (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:482:16)
    at FSReqWrap.oncomplete (fs.js:155:5)
Emitted 'error' event at:
    at FSWatcher.\_handleError (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/index.js:260:10)
    at createFsWatchInstance (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:40:5)
    at setFsWatchListener (/home/chadrick/prj/web/timeline\_test/my-app/node\_modules/webpack-dev-server/node\_modules/chokidar/lib/nodefs-handler.js:81:15)
    \[... lines matching original stack trace ...\]
    at FSReqWrap.oncomplete (fs.js:155:5)
npm ERR! code ELIFECYCLE
npm ERR! errno 1
npm ERR! my-app@0.1.0 dev-start: \`webpack-dev-server\`
npm ERR! Exit status 1
npm ERR! 
npm ERR! Failed at the my-app@0.1.0 dev-start script.
npm ERR! This is probably not a problem with npm. There is likely additional logging output abo
```

which is solved by the final configuration that I used.

## Solution

the final solution config was:

```generic
{

        open: true,
        
        watchOptions:{
            poll: true,
            ignored: "/node\_modules/"
        }
        
    }
```

so the entire webpack.config.js file would be

```generic
var path = require('path');
var HtmlWebpackPlugin =  require('html-webpack-plugin');

module.exports = {
    entry : './src/index.js',
    output : {
        path : path.resolve(\_\_dirname , 'dist'),
        filename: 'index\_bundle.js'
        
    },
    module : {
        rules : \[
            {test : /\\.(js)x?$/, use:\['babel-loader'\]},
            {test : /\\.css$/, use:\['style-loader', 'css-loader'\]}
            
        \]
    },
    mode:'development',
    plugins : \[
        new HtmlWebpackPlugin ({
            template : 'src/index.html',
            
        })
    \],

    devServer: {

        open: true,
        
        watchOptions:{
            poll: true,
            ignored: "/node\_modules/"
        }
        
    }

}
```

and the run script inside `package.json` was:

```generic
"scripts": {
    //... 
    "dev-start": "webpack-dev-server"
  },
```

Here are some explanations with the configuration

- `hot` option is by default on, so I didn’t add `--hot` cli option or added it to the webpack.config.js file under `devServer` section.
- `watchContentBase` is also true by default so I didn’t explicitly specify this option.
- adding `watchOptions` with poll=true, and the `ignored` keyvalue was essential to making it work. adding `ignored: "/node_modules/"` was key for getting rid of the error message I mentioned earlier. I guess the error was caused because something was getting in the way of tracking the entire `node_modules` dir which is not necessary. We only want to track down the source files.
- `open` options is not on by default so you should specify it in `webpack.config.js` file like I did or you could add `--open` command option in the scripts command.

With this setup, I can see that my webpack dev server recompiles and reload the web browser whenever I make changed in `src/index.js` or `src/vis.js`.

## Differences with the informative post

I have learned a lot from the [informative post](https://medium.com/code-oil/burning-questions-with-answers-to-why-webpack-dev-server-live-reload-does-not-work-6d6390277920), but there are some points that I disagree or have done it differently.

- The post said `publicPath` sets the subdomain address where **in-memory** files managed by webpack dev server can be accessed. However the [official doc](https://webpack.js.org/configuration/dev-server/#devserverpublicpath-) mentions nothing about only in-memory files being served thorugh this path, but rather it says this is the explicitly set subdomain path where requests will be able to access the bundled files specified in `output` section. In my solution, I did not touch `publicPath` option since I have no reason to meddle with subdomain path where the necessary files will be served. The default is serving bundled `index_bundle.js` file through `http://localhost:3000/index_bundle.js` and that’s the way I intend to keep it. If I changed the `publicPath` to something like “dist”, then where actual file or in-memory status, the index_bundle.js file will be served through `http://localhost:3000/dist/index_bundle.js` and this would complicate things since this changes need to be applied when creating html file where  tag pointing to index_bundle.js file address. The creation of html file should(*its my guess*) be done by HtmlWebpackPlugin according to my webpack.config.js file, and I have no idea how to make HtmlWebpackPlugin to take these changes into account.
- The subdomain issue is noted in the medium post. And to resolve it, it suggests that the user should manually change the  tag’s src path to e.g. “/dist/index_bundle.js” instead of the default “index_bundle.js”. Apart from the downside of this approach mentioned above, this aroused another complexion. As I said, I’m working on a simple react setup and my html template does not have any  tags pointing to `index_bundle.js` file. The outcome of webpack compiling would have it of course, but the source version of html template does not have it. Here’s my html template in `/src`:

```generic
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My React App</title>
</head>

<body>
    <div id="root"></div>
</body>

</html>
```

As you can see, even if I wanted to follow the instructions of the medium post, I could not. Again, if I really wanted to do something as close to the medium post, I think I should have meddled with the HtmlWebpackPlugin settings, which I’m not sure what to do with. So, if you are also doing a react setup, then I suggest my solution is more appropriate than the medium post.

- The post only set `watchContentBase` without setting appropriate `watchOptions`. Naturally, when I was following the medium post to the letter, I had to face the error messages which was really frustrating.
