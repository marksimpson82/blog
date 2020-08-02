---
id: 611
title: Unit? Integration? Functional? Wha?
date: 2011-02-05T19:39:14+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=611
#permalink: /?p=611
tags:
  - software
  - testing
---
I answered a question titled, “[What’s the difference between unit, functional, acceptance and integration tests?](http://stackoverflow.com/questions/4904096/whats-the-difference-between-unit-functional-acceptance-and-integration-tests)” on Stackoverflow and thought it’d be useful to re-post the answer here for future reference.

<!--more-->

Depending on where you look, you&#8217;ll get slightly different answers.&#160; I&#8217;ve read about the subject a lot, and here&#8217;s my distillation; again, these are slightly woolly and others may disagree.&#160; Indeed, certain companies have their own terminology and categorisations (see [testerab’s answer](http://stackoverflow.com/questions/4904096/whats-the-difference-between-unit-functional-acceptance-and-integration-tests/4908086#4908086))

Depending on where you look, you&#8217;ll get slightly different answers. I&#8217;ve read about the subject a lot, and here&#8217;s my distillation; again, these are slightly wooly and others may disagree.

**Unit Tests**

Tests the smallest unit of functionality, typically a method/function (e.g. given a class with a particular state, calling x method on the class should cause y to happen). Unit tests should be focussed on one particular feature (e.g., calling the pop method when the stack is empty should throw an `InvalidOperationException`). Everything it touches should be done in memory; this means that the test code **and** the code under test shouldn&#8217;t:

  * Call out into (non-trivial) collaborators 
  * Access the network 
  * Hit a database 
  * Use the file system 
  * Spin up a thread 
  * etc. 

Any kind of dependency that is slow / hard to understand / initialise / manipulate should be stubbed/mocked/whatevered using the appropriate techniques so you can focus on what the unit of code is doing, not what its dependencies do. 

In short, unit tests are as simple as possible, easy to debug, reliable (due to reduced external factors), fast to execute and help to prove that the smallest building blocks of your program function as intended before they&#8217;re put together. The caveat is that, although you can prove they work perfectly in isolation, the units of code may blow up when combined which brings us to &#8230;

**Integration Tests**

Integration tests build on unit tests by combining the units of code and testing that the resulting combination functions correctly. This can be either the innards of one system, or combining multiple systems together to do something useful. Also, another thing that differentiates integration tests from unit tests is the environment. Integration tests can and will use threads, access the database or do whatever is required to ensure that all of the code **and** the different environment changes will work correctly. 

If you&#8217;ve built some serialization code and unit tested its innards without touching the disk, how do you know that it&#8217;ll work when you are loading and saving to disk? Maybe you forgot to flush and dispose filestreams. Maybe your file permissions are incorrect and you&#8217;ve tested the innards using in memory streams. The only way to find out for sure is to test it &#8216;for real&#8217; using an environment that is closest to production.

The main advantage is that they will find bugs that unit tests can&#8217;t such as wiring bugs (e.g. an instance of class A unexpectedly receives a null instance of B) and environment bugs (it runs fine on my single-CPU machine, but my colleague&#8217;s 4 core machine can&#8217;t pass the tests). The main disadvantage is that integration tests touch more code, are less reliable, failures are harder to diagnose and the tests are harder to maintain.

Also, integration tests don&#8217;t necessarily prove that a complete feature works. The user may not care about the internal details of my programs, but I do!

**Functional Tests**

Functional tests check a particular feature for correctness by comparing the results for a given input against the specification. Functional tests don&#8217;t concern themselves with intermediate results or side-effects, just the result (they don&#8217;t care that after doing x, object y has state z). They are written to test part of the specification such as, "calling function Square(x) with the argument of 2 returns 4". 

**Acceptance Tests**

Acceptance testing seems to be split into two types:

Standard acceptance testing involves performing tests on the full system (e.g. using your web page via a web browser) to see whether the application&#8217;s functionality satisfies the specification. E.g. "clicking a zoom icon should enlarge the document view by 25%." There is no real continuum of results, just a pass or fail outcome. 

The advantage is that the tests are described in plain English and ensures the software, as a whole, is feature complete. The disadvantage is that you&#8217;ve moved another level up the testing pyramid. Acceptance tests touch mountains of code, so tracking down a failure can be tricky. 

Also, in agile software development, user acceptance testing involves creating tests to mirror the user stories created by/for the software&#8217;s customer during development. If the tests pass, it means the software should meet the customer&#8217;s requirements and the stories can be considered complete. An acceptance test suite is basically an executable specification written in a domain specific language that describes the tests in the language used by the users of the system.

**Conclusion**

They&#8217;re all complementary. Sometimes it&#8217;s advantageous to focus on one type or to eschew them entirely. The main difference for me is that some of the tests look at things from a programmer&#8217;s perspective, whereas others use a customer/end user focus.