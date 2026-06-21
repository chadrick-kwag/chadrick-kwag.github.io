---
title: basic react project setup configurations
date: '2020-03-28T00:00:00+00:00'
lastmod: '2020-03-28T00:00:00+00:00'
slug: basic-react-project-setup-configurations
categories:
- web
tags: []
draft: false
---
## npm install commands

```generic
$ npm i --save-dev react react-dom webpack webpack-dev-server html-webpack-plugin babel-loader style-loader css-loader @babel/core @babel/preset-env @babel/preset-react webpack-cli
```

## add `babel.config.json`

```json
{
    "presets": \["@babel/preset-env", "@babel/preset-react"\]
}

```

## add `webpack.config.js`

```js
     const hwp = require('html-webpack-plugin')
    const path = require('path')

    module.exports = {
  mode: 'development',
        entry: './src/app.js',
        output: {
            path: path.resolve(\_\_dirname, 'dist'),
            filename: 'bundle.js'
        },
        module:{
            rules:\[
                {
                    test: /\\.jsx?$/,
                    include: path.resolve(\_\_dirname, 'src'),
                    exclude : "/node\_modules",
                    use: "babel-loader"
                },
                {
                    test: /\\.css/,
                    use: \["style-loader", "css-loader"\]
                }
            \]
        },
        plugins: \[
            new hwp({
                template: "./src/template.html"
            })
        \],
        devServer:{
            open: "chrome",
	    compress: false

        }
    }

```
