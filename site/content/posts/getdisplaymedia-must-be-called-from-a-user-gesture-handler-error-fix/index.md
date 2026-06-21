---
title: '"getDisplayMedia must be called from a user gesture handler" error fix'
date: '2020-03-04T00:00:00+00:00'
lastmod: '2020-03-04T00:00:00+00:00'
slug: getdisplaymedia-must-be-called-from-a-user-gesture-handler-error-fix
categories:
- web
tags:
- error
- getdisplaymedia
- javascript
- user-gesture-handler
draft: false
---
# Problem

While implementing screen capture which requires the use of `navigator.mediaDevices.getDisplayMedia` function, I contronted an error as a result of a promise returned from `getDisplayMedia`. The following is the javascript code that calls `getDisplayMedia` function and the output from the console which contains the error object returned as a result of the `getDisplayMedia` promise.

```js
// js code
document.addEventListener('DOMContentLoaded', function(){
    console.log("dom load complete")

    let capturestream = null
    var mediaoption = {
        video: true,
        audio: false
    }
    try{
        let result = navigator.mediaDevices.getDisplayMedia(mediaoption)
        console.log(result)
        result.then(function(res){
            console.log(res)
            console.log(result)
        }, function(err){
            console.log(err)
            console.log(result)
        })

    }
    catch(err){
        console.log(err)
    }

})
```

```generic
// console output
MediaStreamError { name: "InvalidStateError", message: "getDisplayMedia must be called from a user gesture handler.", constraint: "", stack: "" }
```

# Cause & Solution

I tried to call `getDisplayMedia` function at an event which does not require user’s explicit action. My current implementation is triggered when page loading is finished which is automatic and does not require any action from user. `getDisplayMedia` fuction must be triggered from an event handler that is triggered by a user’s action such as button clicking. Therefore a simple solution is to call `getDisplayMedia` from a button click handler.

I added a button on the html with id=“capturebtn” and changed the javascript code to the following.

```js
    document.getElementById("capturebtn").onclick=function () {
        console.log("dom load complete")

        let capturestream = null
        var mediaoption = {
            video: true,
            audio: false
        }
        try {
            let result = navigator.mediaDevices.getDisplayMedia(mediaoption)
            console.log(result)
            result.then(function (res) {
                console.log(res)
                console.log(result)
            }, function (err) {
                console.log(err)
                console.log(result)
            })

        }
        catch (err) {
            console.log(err)
        }

    }
```

Aftr this modification, when I click the button now I get the following from the console.

```generic
MediaStream { id: "{72e96826-30f7-4282-861b-311ed7d0b3f6}", active: true, onaddtrack: null, onremovetrack: null }
```
