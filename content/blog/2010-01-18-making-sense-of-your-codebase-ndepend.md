---
id: 482
title: "Making sense of your codebase: NDepend"
date: 2010-01-18T01:53:04+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=482
#permalink: /?p=482
tags:
  - 'c#'
  - software
  - ndepend
---
I was given an NDepend license to play around with (thanks to Patrick) and said I'd blog about it. Apologies for my tardiness!

### What is NDepend?

[NDepend](http://www.ndepend.com/Features.aspx) is a piece of software that allows developers to analyse and visualise their code in many interesting ways. Here's an ancient relic from my hard drive, revived in NDepend:

[<img class="alignnone" src="images/whole_app_thumb.png" alt="" width="326" height="228" />](images/whole_app.png)

As you can see, there's quite a lot of functionality included. NDepend includes features that allow you to trawl your code for quality problems, identify architectural constraints that have been breached, find untested, complicated code or pinpoint changes between builds and much more. This post will merely scratch the surface, but will hopefully provide some decent information on what NDepend can do for you and your team.

NDepend works with Visual Studio solution files and integrates with Visual Studio, meaning it's simple to generate an NDepend project based on a solution. You can then press the analyse button and watch NDepend do its thing - it generates a nice HTML report with various visualisations and statistics.

### CQL all the way

NDepend provide a lot of pre-defined metrics out of the box, but its best feature by far (and the one on which most of its functionality is built) is the CQL query language. The SQL / Linq-esque query language allows you to search, filter and order data in a simple fashion. Once you get accustomed to the query language, it is simple to start bashing out meaningful queries.

You enter queries into a command window and the results are displayed instantly. For example, you could write something like this:

<img class="alignnone" title="CQL query" src="images/sample_cql_query.png" alt="" width="413" height="82" /> 

At the time of writing, 82 separate metrics are available; the metrics are grouped by categories including: assembly, namespace, method etc. If you have an idea, then you can probably express that idea via CQL.  Furthermore, your queries can be saved and reused/applied to projects as required.

To write a query, you just tap it into the query editor:

<img class="alignnone" title="editor" src="images/query_editor.png" alt="" width="465" height="221" /> 

### Don't be Paralysed by Choice

While it is a hugely powerful program, I found it overwhelming to begin with. The default analysis of your code will result in a verbose report including every metric under the sun; some of these are unarguably very useful (Cyclomatic complexity, IL nesting depth) whereas others have a more narrow purpose (suggesting which attributes should be sealed, boxing and unboxing warnings and so on).

Due to the mammoth amount of information in the report, it's akin to pulling the FxCop lever for the first time. You get metrics-shotgunned in the face and potentially paralysed by choice. As a result, I chose to view the default report as a rough guide for how to use the CQL query language and to give me ideas of how I could form queries that were tailored to my needs. There's an excellent [placemat PDF available for download](http://www.hanselman.com/blog/content/binary/NDepend%20metrics%20placemats%201.1.pdf), too.

I would encourage first time users to skim the main report for interesting nuggets then immediately begin to play around with the CQL query language :). It's really cool to think, "I wonder if...", type a few words and immediately see the question answered.

### Manual trawling versus NDepend

Back when I was a Test Engineer, I was assigned to look at an unfamiliar part of our codebase. I decided to do a little experiment using NDepend to determine its effectiveness (we have a few licenses at work too and are looking to integrate it into our build process at some stage soon). The test was simply this: I would work through the code manually checking each file/type for problems, then I would do a sweep using NDepend to see if it could pick out the same problems (and potentially some others I'd missed).

The sort of things I was looking for included:

  * Big balls of mud / God classes
  * Types with the most complicated functionality (high cyclomatic complexity / code nesting level)
  * Types that are heavily used ('arteries' of the codebase - failure would be more costly)
  * Types that have poor coverage and high complexity

The results were good. The majority of the problems I had identified during a manual sweep showed up near the top of the query results. It took me a few hours to manually trawl a relatively small portion of the codebase. It took me about an hour to get to grips with the NDepend basics, write some CQL and make sense of the results. I'd say that's very good going considering I hadn't used it before.

One thing to watch out for is that some manual tweaking is often required as, if you have some ugly utility classes or use open source software in source form (such as the command line argument parser class that is ubiquitous at work), these sorts of thing monopolise the results. To get around this problem you can ignore these types, either by applying attributes to your types in code, or by adding an explicit exclude via your query (some examples of which are included below).

### Sample Queries

Here's a few examples of how to express the aforementioned concerns as queries. Note: I'm an NDepend newbie, so there's probably better ways to do this.

**Types that have so many lines of code that it makes your head spin**

<img title="God" src="images/god_classes.png" alt="" width="413" height="82" /> 

**Complicated nesting**

<img class="alignnone" title="nesting" src="images/il_nesting.png" alt="" width="413" height="82" /> 

**Complicated methods**

<img class="alignnone" title="nesting" src="images/complex_methods.png" alt="" width="413" height="82" /> 

**High complexity with poor test coverage**

<img class="alignnone" title="nesting" src="images/poor_coverage.png" alt="" width="413" height="82" /> 

**'Popular' types with poor test coverage**

<img class="alignnone" title="nesting" src="images/popular_types.png" alt="" width="413" height="82" /> 

None of these are 'hard' rules - you have to play around with them while browsing your codebase (which is easy as NDepend's CQL editor is constantly updating as you enter the query). You may find that one project has really simple code that doesn't even register on a solution-wide analysis, whereas another project may hog the results pane. If you have a specific goal in mind, you can iteratively tailor the query to get what you want :).

### The role of NDepend?

NDepend is not a silver bullet and doesn't claim to be - it's a complementary tool that can be used in addition to buddy systems, code reviews and so forth. Having said that, the amount of information you can mine from your codebase is pretty impressive.

In terms of practical usage, we plan to integrate it into our build system to aid us in identifying potential problems, including code changes not backed by tests, architectural rules (project x is not allowed to reference project y) and general rules of thumb that should be respected (cyclomatic complexity, nesting depth and so forth).

In short, it's well worth checking out NDepend.