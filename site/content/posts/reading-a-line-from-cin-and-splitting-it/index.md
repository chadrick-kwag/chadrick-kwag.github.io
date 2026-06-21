---


title: reading a line from cin and splitting it
date: '2018-12-09T00:00:00+00:00'
lastmod: '2018-12-09T00:00:00+00:00'
slug: reading-a-line-from-cin-and-splitting-it
categories:
- python
tags:
- "reading"
- "line"
- "cin"
- "splitting"
draft: false
---
```cpp
#include "pch.h"
#include <iostream>
#include <iterator>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int main()
{
	
	string something;

	getline(cin, something);

	cout << "saved string: " << something;

	istringstream iss(something);
	
	vector<string> results(istream\_iterator<string>{iss}, istream\_iterator<string>());

	cout << "results size: " << results.size() << '\\n';

	for (int i = 0; i < results.size(); i++) {
		cout << results.at(i);
	}

	return 0;
}
```
