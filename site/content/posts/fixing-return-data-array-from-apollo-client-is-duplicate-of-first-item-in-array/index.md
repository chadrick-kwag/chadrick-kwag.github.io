---
title: fixing return data array from apollo client is duplicate of first item in array
date: '2020-08-11T00:00:00+00:00'
lastmod: '2020-08-11T00:00:00+00:00'
slug: fixing-return-data-array-from-apollo-client-is-duplicate-of-first-item-in-array
categories:
- web
tags:
- apollo-client
- first-item-of-array-duplicate
draft: false
---
## Situation

I am querying with apollo client to fetch some userinfo. From the server side which uses apollo server, I can check that it is returning an array of two items which have different contents.

However, when I console the fetched data from apollo client, the array is somehow incorrect. The length of the array is correct, but the items are not. It became an array of two identical items, which is the first item that has been sent from the server.

## Solution

I was using `network-only` as fetchPolicy for my apollo client queries. As it turns out, `netowrk-only` isn’t what I thought it was. This fetch policy will check in with the server but its results will be saved in cache and then the data from the cache will be served to the apollo client response. The data was corrupted during “saved cache->apollo client response” stage. While caching the data from network response, it uses `id` of received objects to discriminate one another. However, my GQL structure is twofold where the array type return has a sibling. So from the root’s point of view, there is no field `id` and thus it will return `undefined` when the cache process accesses the `id` of the return object. I think this is what is screwing up proper caching.

The solution was simple. Change fetchPolicy to `no-cache`. This variant will skip saving the network response to cache procedure and directly serve the network response to apollo client query. This way, nothing will tamper with the correct network response.
