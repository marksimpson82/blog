---
id: 377
title: Understanding test doubles
date: 2009-08-22T16:10:36+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=377
#permalink: /?p=377
tags:
  - 'c#'
  - testing
  - tips
---
There is a bewildering array of types of 'mock' object available to a tester. The canonical list of test doubles was probably coined by the venerable Martin Fowler in his article ["Mocks Aren't Stubs"](http://martinfowler.com/articles/mocksArentStubs.html) and, to me, this list is fairly complete and makes sense. The reason it makes sense is that I've manually written classes that perform these roles.

  * I needed to fill out a parameter list with non-null objects, so I created a dumb class with absolutely no implementation.
  * I wanted to listen in on additions to a list, so I wrote a class that stored the objects, acting as a spy.
  * I wanted to provide canned results to test another part of my system, so I wrote a stub.
  * I needed to ensure a method was called, so I wrote a Mock.
  * I needed a coherent, fast implementation of a class, so I wrote a fake implementation.

My problem with testing terminology is that it's harmful to newcomers, especially when the semantics affect the result of the test! Not only is there a high barrier to entry when it comes to writing accurate, robust and maintainable tests, but the terminology is another unwelcome complication.

For this reason, I personally advocate keeping new testers away from mocking frameworks until they've become comfortable with state-based testing and hand-rolled a variety of their own test doubles.

### Information Overload

Even when no additional frameworks are involved (i.e. when using vanilla xUnit), writing good unit tests involves a steep learning curve. It's easy to take a wrong turn and the quality of the tests written will improve only with experience/guidance. I was not surprised when I read [Roy Osherove's blog](http://weblogs.asp.net/rosherove/archive/2008/09/20/goodbye-mocks-farewell-stubs.aspx) and discovered that the majority of organisations' attempts to embrace unit testing resulted in failure.

Mocking frameworks like Rhino Mocks are absolutely excellent tools, but it's yet another thing to learn. Suddenly the type of object (mock, strict mock, stub etc.) affects the result of the test. It took me a week to get my head around it, so it doesn't surprise me when I see newcomers totally abusing these frameworks. Not only does this create a maintenance nightmare, but it sours their first taste of testing.

The problem is doubly hard to tackle, as Mocking frameworks allow you to write the same tests with fewer lines of code. Developers who are new to testing see this and immediately try to use the mocking framework. After all, only a fool would eschew such benefits, right? Well, some people just 'get it' from the start. I'm not one of these people and, in my experience, nor are most others. Starting with interaction based testing and mocking frameworks is akin to throwing someone out of the back of a van that's moving at 70mph and expecting them to start running when they hit the tarmac. Chances are they're going to land on their face.

The unfortunate result is that some folk tie themselves in knots. They don't understand the responsibilities of each type of testing object and, as a result, create extremely brittle or utterly pointless tests. If you have no idea of what you're trying to achieve with a test, there is no point in writing it. I once saw a question on StackOverflow featuring a confused fellow asking why his test did not work. The poster was using Rhino Mocks and created a Mock of the _class under test_. I.e. it was not a collaborator, it was the **class under test** and he was mocking it! I suspect he was simply overwhelmed by trying to learn multiple new things.

Other things I've witnessed include developers writing obscure lambda expressions using c#, then chaining together RhinoMocks methods to perform something which _somehow_ works. When I pointed out that I could barely infer its purpose by reading the code and that writing a hand rolled stub would probably be a better idea, I was met with "yes, you're probably right but I want to use Rhino Mocks".

Warning bells should also start ringing when you return a mock and assert that its method was called by another mock which returns a mock which... errrr! It's much easier to make a dog's dinner of interaction-based testing; a good grounding in state-based testing is essential.

### One step at a time
1. Learn to sit up before you crawl. Write simple xUnit tests that involve state-based testing. It doesn't have to be great, isolated code. Even writing tests that involve scores of classes is a good way to start. Finer granularity is something that comes with experience.
2. Crawl before you walk. Start to experiment and find better ways of testing pieces of functionality. Ask yourself whether the test is useful, maintainable etc. Will other parts of the system break it if they change? Can you make the components and tests themselves finer grained? This stage should be about developing your sense of what constitutes a good test.
3. Walk before you run. Begin to experiment with different types of test doubles, but **hand roll them**. Yes, it's painful at times, but it will give you a better understanding of roles in tests and the different types of test doubles, even if you don't have names for them yet. Furthermore, constantly having to update your hand rolled stubs when disparate parts of your class changes will also give you an appreciation for the [interface segregation principle](http://www.globalnerdy.com/wordpress/wp-content/uploads/2009/07/interface_segregation_principle.jpg).
4. Finally, install a mocking framework and start sprinting.

If you do sprint head-first into a wall, you will be better equipped to understand where you went wrong, as you understand the fundamentals. You will also have a better grasp of the terminology, as it will be grounded in real, tangible code you've written.