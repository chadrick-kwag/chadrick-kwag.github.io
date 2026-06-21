---


title: vue list item toggle class on click example
date: '2019-01-03T00:00:00+00:00'
lastmod: '2019-01-03T00:00:00+00:00'
slug: vue-list-item-toggle-class-on-click-example
categories:
- web
tags:
- "vue"
- "list"
- "item"
- "toggle"
- "class"
draft: false
---
```html
<div>
    <ul class="list-group">
        <li class="list-group-item" v-for="(item,index) in items" @click="toggle\_active(item)" :key="index" v-bind:class="{active: item.isActive}">
            ${item.dirname}
        </li>
    </ul>
</div>
```
