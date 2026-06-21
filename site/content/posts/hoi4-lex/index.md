---
title: hoi4 lex
date: '2019-01-10T00:00:00+00:00'
lastmod: '2019-01-10T00:00:00+00:00'
slug: hoi4-lex
categories:
- tools
tags: []
draft: false
---
```generic
import re, sys

testfile = "test.save.txt"

with open(testfile,'r') as fd:
    
    chars = fd.read()

def lex(chars, token\_expr\_list):

    pos=0
    tokens=\[\]
    while pos < len(chars):
        match=None
        for token\_expr in token\_expr\_list:
            pattern, tag = token\_expr
            r = re.compile(pattern)
            match = r.match(chars,pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                    print("token : {}".format(token))
                break
            
        if not match:
            print("error with : {}".format(pos))
            sys.exit(1)
        
        else:
            pos = match.end(0)

    return tokens

# for line in all\_lines:
#     print(line)    

token\_expr\_list = \[
    (r'\[ \\n\\t\]+', None),
    (r'=\[ \\n\\t\]\*{',"ITEM\_START"),
    (r'}',"ITEM\_END"),
    (r'\[0-9\\.\]+','NUM'),
    (r'\[a-zA-Z0-9\_\]+','STRING')

\]

tokens = lex(chars, token\_expr\_list)

print(tokens)

    

print("finish")
```
