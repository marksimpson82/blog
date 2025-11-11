---
id: 753
title: Python data-driven testing, ddt and @unpack
date: 2014-03-09T15:31:05+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=753
#permalink: /?p=753
tags:
  - python
  - software
  - testing
  - tips
---
Several eons ago, [I wrote a blog post]({% post_url 2012-05-21-data-driven-testing-with-python %}) about using 
the python ddt package. My only criticism was that you had to manually pack/unpack the test case arguments.

Happily, the developers of ddt were nice enough to add an @unpack decorator! You can now provide lists/tuples/dictionaries and, via the magic of @unpack, the list will be split into method arguments.

Documentation is here: [http://ddt.readthedocs.org/en/latest/example.html](http://ddt.readthedocs.org/en/latest/example.html "http://ddt.readthedocs.org/en/latest/example.html")