---
id: 110
title: "Code coverage: What it is and what it isn't"
date: 2009-03-30T22:34:25+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=110
#permalink: /?p=110
tags:
  - testing
  - coverage
---
## Coverage

I recently posted a [stack overflow answer](http://stackoverflow.com/questions/695811/pitfalls-of-code-coverage/695888#695888) detailing why imposing coverage requirements can have a negative impact. I think it's worth recycling here.

## What is coverage?
In grossly simplified terms, code coverage tells you how much of your code was executed when your test suite (typically unit tests) is run. <a href="http://en.wikipedia.org/wiki/Code_coverage">There are different kinds of coverage</a>, but in my experience, most people seem to focus on lines of code as opposed to anything more complicated. I'm not going to delve into anything more complicated regarding what coverage is. There's plenty of articles out there that explain it better than I can. Instead, I wish to describe some of the potential caveats that come with striving for high levels of coverage.

### How should I view coverage?
Code coverage tells you what you definitely <strong>haven't</strong> tested, not what you <strong>have.<br /> </strong>

Part of building a valuable unit test suite is finding the most important, high-risk code and asking hard questions of it. You want to make sure the tough stuff works as a priority. Coverage figures have no notion of the 'importance' of code, nor the quality of tests. High levels of coverage can be obtained by writing tests that assert on nothing meaningful or do not assert on anything at all, and yet it will be included in the coverage. The only thing coverage proves in these cases is that the code was run and didn't throw an exception. Big deal.

Many of the most important tests you will ever write are the tests that barely add any coverage at all.

### In context  
Today, I was writing some unit tests for part of a scheduler I'm creating. The first few tests I wrote (in a minute or two) probably obtained 85% coverage or more in one of my recurrence rules class - it's a relatively small class with few dependencies.  The tests passed and I bathed in the glow of the NUnit's green bar. 

However, although the obvious cases worked, obvious is not interesting. Obvious is not the stuff that generally fails, nor is it the logic that is hellish to debug (especially when you return to it months later and have to re-acquaint yourself with the code).
I then spent about a half an hour writing test case after test case containing edge cases where dates overlapped slightly, or the initial scheduled date had not yet been reached, or the start date was after the end date etc. Red, red, red. Damn. Lots and lots of bugs. 

Most of them were simple errors that I could fix easily, but they were errors nonetheless. An hour or two later I had fixed my recurrence rules and also written even more tests for extra edge cases. In doing so, I probably added a paltry 5% to my coverage. So the 85% coverage looked really nice, but ultimately proved that the obvious cases worked. It was the <em>other</em> 5% of coverage that proved to be invaluable. The trouble is, to NCover or any piece of coverage software, each percentage point is indistinguishable from the next. Coverage is not qualitative.

### More potential drawbacks
Another problem with setting hard coverage targets is that developers may have to start bending over backwards to test their code to reach the appropriate levels of coverage. There's making code testable (which I fully approve of!) and then there's torture. If it is easy to test something up to 100% and you are writing meaningful and useful tests, go for it. However, in most situations the extra effort is just not worth it - there comes a point of diminishing returns beyond which the pain of eeking out those last few percentage points could be spent writing more code, or writing more useful tests for other code.

Every assembly, class and method is different, so setting a <strong>rigid </strong>goal is something I disagree with, unless there's a very good reason for it (e.g. You're working at NASA writing the code that will fire the shuttle boosters...)

### Don't confuse quantity and quality
If you set an unrealistic goal, deadlines are approaching and the target looks hard to achieve, folk will just write rubbish tests to 'top up' to the target coverage levels. I'd much rather have a solid set of tests and 65% of coverage than down-the-middle tests and 95% coverage. If the 65% coverage tests exhaustively test a smaller, more important/fragile/regression prone part of a project, then they are much more valuable. Period.
Just remember what the point of automated testing is - <strong>to help make sure your software works</strong>. A tick next to your coverage figure does not prove this. Good, varied testing goes a long way towards it, though.

### What coverage *is* good for
Again, I tend to look at coverage as a coarse indicator of what definitely <strong>hasn't</strong> been tested. If you find out that project x has no tests in area y, then it immediately becomes obvious that there's a hole in the test suite. You know by the lack of coverage that tests should be written. Similarly, if I can look at a method body and some important paths are not being tested, then they stick out like a sore thumb. So, when properly applied, coverage can be a very useful tool for getting a snapshot of the testing status at multiple levels of granularity, but it should be used as a guide, not as an absolute measure.</div>