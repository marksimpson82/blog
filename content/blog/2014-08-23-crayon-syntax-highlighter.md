---
id: 794
title: Crayon syntax highlighter
date: 2014-08-23T22:20:08+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=794
#permalink: /?p=794
tags:
  - Uncategorized
---
I've tried to install a couple of different syntax highlighters in the past and was thoroughly unimpressed. They either failed to install cleanly, didn't work or had numerous issues that rendered them useless.

Anyway, after manually formatting source code snippets for years, I'm giving Crayon a go. The install was easy and the output looks good. Let's see how we go :-)

```c++
class Test
{
  int x;
  std::string hi;

public:
  Test(int x, std::string hi)
  : x(x), hi(hi)
  {

  }
}
```

You can find it here: [https://wordpress.org/plugins/crayon-syntax-highlighter/](https://wordpress.org/plugins/crayon-syntax-highlighter/)