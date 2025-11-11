---
id: 632
title: Unity3d - Threadpool Exceptions
date: 2011-08-27T15:11:48+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=632
#permalink: /?p=632
tags:
  - 'c#'
  - debugging
  - gotchas
  - software
  - tips
  - Unity3d
---
A quickie, but something to be _very_ wary of. I’ve been using Unity3d of late (I recommend it – it’s a very opinionated and sometimes quirky bit of software, but it generally works well) and I was recently tasked to parallelise some CPU intensive work. 

I decided, quite reasonably, to use the built-in [ThreadPool](http://msdn.microsoft.com/en-us/library/system.threading.threadpool.aspx) rather than doing my own explicit management of threads, mainly because the work we’re parallelising is sporadic in nature, and it’s easier to use the ThreadPool as a quick first implementation. So far, so good. Everything was going swimmingly, and it appeared to work as advertised. In fact, the main implementation took less than a day.

Most .NET developers who are familiar with doing threading with the ThreadPool will know that, post .NET 1.1, if an unhandled exception occurs on a ThreadPool thread, the default behaviour of the CLR runtime is to [kill the application](http://msdn.microsoft.com/en-us/library/ms228965.aspx). This makes total sense, as you can no longer guarantee a program’s consistency once an unhandled exception occurs. 

To cut a long story short, I spent about three days debugging a very subtle bug with a 1 in 20 reproduction rate (oh threading, how I love thee). Some methods were running and never returning a result, yet no exceptions were reported. 

Eventually I reached a point where I’d covered nearly everything in my code and was staring at a [Select Is Broken](http://www.codinghorror.com/blog/2008/03/the-first-rule-of-programming-its-always-your-fault.html) situation (in that Unity3d had to be doing something weird).

**Unity3d silently eats ThreadPool exceptions!** I proved this by immediately throwing an exception in my worker method and looking at the Unity3d editor for any warnings of exceptions – none was reported (at the very least, they should be sending these exceptions to the editor). 

I then wrapped my worker code in a try catch and, when I finally got the 1 in 20 case to occur, sure enough, there was an exception that was killing my application’s consistency. So yes, I _did_ have a threading bug in my application code, but Unity3d’s cheerful gobbling of exceptions meant the issue was hidden from me.

I’ve [bugged the issue](http://fogbugz.unity3d.com/default.asp?416782_1n7rsv4g9vrudomi), so hopefully it’ll get fixed in future.

**Note:** To the people who say “you should be handling those exceptions in the first place”, I would say, “not during development”. When developing, I generally _want_ my programs to die horribly when something goes wrong, and that is the expected behaviour for the .NET ThreadPool. Unhandled exceptions make it clear that there’s a problem and it means the problem must be fixed.