---
id: 726
title: 'The fundamentals of unit testing : Use factory methods!'
date: 2012-11-11T06:03:47+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=726
#permalink: /?p=726
tags:
  - fundamentals of unit testing
  - testing
  - tips
---
Tests are just like normal code in the sense that repeating yourself can cause problems.&#160; Practically every single call to new in a test method is a maintenance risk. 

## A Simple Illustration of the Problem

Say we have 30 tests, each directly invoking constructors like the following example:

> [Test]  
> public void when\_adding\_a\_valid\_order\_it\_is\_appended\_to\_audit\_trail()  
> {  
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; var orderService = new OrderService(); // hello Mr. Constructor
> 
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; &#8230; // rest of test  
> }

It doesn’t look so bad but, if in 3 months, OrderService is changed to use constructor injection and its interface is changed to include a new “Start” method that must be called prior to certain methods being usable, we have a problem. Now we have 30 broken tests that must be fixed individually.&#160; I once had to clean up hundreds of tests broken by a single constructor call.&#160; It wasn’t fun.&#160; Or productive.

## A Solution

I say “a solution” as there are other ways to tackle this problem, such as using test framework setup methods / test data builders etc.&#160; However, this is the easiest way to get started and is the approach I tend to reach for in the majority of cases.&#160; I’ll blog about why I tend to eschew framework setup methods later.

We can insulate our tests from breaking changes by moving object creation to simple private factory methods. It is then often a case of updating the factory method once.

> [Test]  
> public void when\_adding\_a\_valid\_order\_it\_is\_appended\_to\_audit\_trail()  
> {  
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; // Arrange  
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; var orderService = CreateOrderService();
> 
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; &#8230; // rest of test  
> }
> 
> private OrderService CreateOrderService()  
> {  
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; var orderService = new OrderService(new StubLogger(), new MessageGateway());  
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; orderService.Start();
> 
> &#160;&#160;&#160;&#160;&#160;&#160;&#160; return orderService;  
> }

## Benefits

This has tangible benefits. Firstly, it only takes maybe 5 seconds of work (extract method using ReSharper) to create the factory method, but it can save literally hours of work down the line. 

Secondly, the tests and the creation of objects are separated to improve maintainability. 

Thirdly, it often makes the test code easier to read. If the factory method were inlined in the test code, it adds a load of noise. All the test needs is a default configuration of the order service. We only worry about the details if it&#8217;s relevant. Most test fixtures only need a handful of factory methods; for those that require more varied configurations, check out the [Test Data Builder](http://c2.com/cgi/wiki?TestDataBuilder) and [Object Mother](http://c2.com/cgi/wiki?ObjectMother) patterns (though be wary of over-using the Object Mother pattern as not only does it have a stupid name, but it’s inflexible and has other problems) .&#160; 

An alternative to this approach is to use a parameterised factory method and/or optional parameters.

In terms of cost/benefit trade-offs, creating one or more factory methods is a simple, easy technique.&#160; Now when constructors change, you don’t spend half an hour fixing up constructor calls.