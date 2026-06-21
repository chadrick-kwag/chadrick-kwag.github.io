---
title: get timestamp in javascript
date: '2020-03-10T00:00:00+00:00'
lastmod: '2020-03-10T00:00:00+00:00'
slug: get-timestamp-in-javascript
categories:
- web
tags:
- javascript
- timestamp
draft: false
---
unfortunately there isn’t any native way to get formatted timestamp. Here is a script that does the job.

```js
var d = new Date()

let \[h,m,s\] = d.toLocaleTimeString().split(':')

let \[year,month,day\] = d.toLocaleDateString().split('-')

if(year.length >2){
    year = year.slice(2)
}

if(month.length<2){
    month = '0'+month
}

if(day.length <2){
    day = '0' + day
}

timestamp = year+month+day+'\_'+ h+m+s
```

this will output YYMMDD_HHMMSS format timestamp
