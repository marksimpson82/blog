---
id: 369
title: Getting up and running with Fluent NHibernate
date: 2009-08-19T23:01:54+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=369
#permalink: /?p=369
tags:
  - 'c#'
---
I&#8217;ve been meaning to try out NHibernate for a good ol&#8217; while.  It&#8217;s a long-established and respected O/R M library and one of the authors (Ayende) writes a blog that I&#8217;ve read for a long time.

Anyway, NHibernate is great, but its object => db mappings are a bit of a pain.  They are based on xml which is verbose, fiddly to write and the separation makes refactoring and testing mappings somewhat hard.  There are other ways to create mappings in code, such as via attributes, but this approach pollutes your business objects with DB specific code and still doesn&#8217;t help with the testing issue.  This and the lack of a LINQ to NHibernate are the only two main gripes I&#8217;ve heard about NHibernate.  The latter problem is getting solved for the next release.

The weakly typed mappings solution is already most of the way there.  Step forward [Fluent NHibernate](http://fluentnhibernate.org/).  Fluent NHbernate alleviates these problems by providing both convention based auto mappings and mappings created via strongly-typed code.  Lots of blogs and articles cover Fluent NHibernate; the point of this post is to point out a few gotchas that may occur when getting up and running.

Firstly, the FluentNhibernate example project does not have all of the required assemblies when you try to run it.  If you check the InnerException message, it&#8217;s clear which assemblies are missing.  From memory, it&#8217;s one of the byte code .dlls.  Either set up an assembly reference or create a postbuild step to copy it.

Moving on:

When writing my own Noddy sample application, I followed [This Tutorial](http://dotnetslackers.com/articles/ado_net/Your-very-first-NHibernate-application-Part-1.aspx) and, while it is good, it misses out a few things:

**Gotcha #1:** 

If you use SQLite to run your application and/or test your mappings, the version of SQLite provided with Fluent NHibernate is an x86 assembly.  If you have a 64 bit OS and fail to build your project in x86 mode, you&#8217;ll get various obscure error messages (instead of a BadImageFormatException or whatever .NET usually throws).  The solution to this particular problem is to set the project(s) to build in x86 mode.

**Gotcha #2:**

The following line will also cause an exception (or at least it did on my PC &#8212; running 64 bit Windows 7):

Id(c => c.Id).GeneratedBy().HiLo(&#8220;customer&#8221;);

Again, it&#8217;s a very vague exception.  The article has someone seeking help for the same problem, but no solution.  I asked on StackOverflow and the solution is to either remove the trailing .GeneratedBy&#8230;. fluent method calls, or to [replace it with something like HiLo(&#8220;1000&#8221;).](http://stackoverflow.com/questions/1283210/fluent-nhibernate-mappingexception-could-not-instantiate-id-generator)

There may be implications for making such a change, but when you just want to get a Noddy application up and running so you can do a bit of fiddling about, it&#8217;ll do the job. :)