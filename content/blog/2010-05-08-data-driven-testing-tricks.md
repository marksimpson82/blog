---
id: 534
title: Data-driven testing tricks
date: 2010-05-08T21:12:08+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=534
#permalink: /?p=534
tags:
  - 'c#'
  - patterns
  - testing
  - tips
  - data-driven
---
It's a fairly common occurrence - somebody wants to use NUnit's data driven testing, but they want to vary either the action under test, or the expectation. I.e. they're not parametrising simple _data_, they're parametrising the _actions_.

You cannot encode these things via normal data-driven testing (short of doing really nasty things like passing string names of methods to be invoked or using enums and a dictionary of methods) and even if you use a hackish workaround, it's unlikely to be flexible or terse.

Test readability is paramount, so if you have some tests written in an unfamiliar style, it is very important to express the intent clearly, too.

**NUnit's data-driven testing**

NUnit uses a few mechanisms to parametrise tests. Firstly, for simple test cases, it offers the 
[TestCase](http://nunit.org/?p=testCase&r=2.5) attribute which takes a `params object[]` array in its constructor. Each 
argument passed to the TestCaseAttribute's constructor is stored, ready for retrieval by the framework. 

NUnit does the heavy lifting for us and casts/converts each argument to the test method's parameter types. Here's an 
example where three ints are passed, then correctly mapped to a test method:

<img class="alignnone" src="images/simple_data_driven.png" alt="" width="689" height="361" /> 

The main limitation here is that we can only store intrinsic types. Strings, ints, shorts, bools etc. We can't new up classes or structs because .NET doesn't allow it. How the devil do we do something more complicated?

### Passing more complicated types

It would appear we're screwed, but fortunately, we can use the 
[TestCaseSource](http://www.nunit.org/index.php?p=testCaseSource&r=2.5) attribute. There are numerous options for 
yielding the data, and one of them is to define an IEnumerable<TestCaseData> as a public method of your test class (it 
works if it's private, but since it's accessed via reflection it's a good idea to keep it public so that ReSharper or 
other tools do not flag it as unused). 

You can then fill up and yield individual TestCaseData instances in the same 
fashion as before. Once again, NUnit does the mapping and the heavy lifting for us.

<img class="alignnone" src="images/passing_more_complicated_types.png" alt="" width="604" height="379" /> 

If you do not require any of the fancy SetDescription, ExpectedException etc. stuff associated with the TestCaseData type, you can skip one piece of ceremony by simply yielding your own arbitrary type instead (i.e. change the IEnumerable<TestCaseData> to IEnumerable<MyType> and then simply yield return new MyType()).

### Passing a delegate as a parameter (simple)

The simplest case is that you want to vary which methods are called. For example, if you have multiple types implementing the same interface or multiple static methods, encoding which method to call is very simple.

Here's an example from Stackoverflow that [I answered recently](http://stackoverflow.com/questions/2784685/how-do-i-simplify-these-nunit-tests/2784829#2784829) where the author wanted to call one of three different static methods, each with the same signature and asserts. The solution was to examine the method signature of the call and then use the appropriate Func<> type ([Funcs and Actions are convenience delegates provided by the .NET framework](http://msdn.microsoft.com/en-us/library/018hxwa8.aspx)). It was then easy to parametrise the test by passing in a delegates targeting the appropriate methods.

<img class="alignnone" src="images/passing_delegates.png" alt="" width="584" height="443" /> 

### More advanced applications

Beyond calling simple, stateless methods via delegates or passing non-intrinsic types, you can do a lot of creative and cool stuff. For example, you could new up an instance of a type T in the test body and pass in an Action<T> to call. The test body would create an instance of type T, then apply the action to it. You can even go as far as expressing Act/Assert pairs via a combination of Actions and mocking frameworks. E.g. you could say "when I call method X on the controller, I expect method Y on the model to be called", and so forth.

The caveat is that as you do use more and more 'creative' types of data-driven testing, it gets less and less readable for other programmers. Always keep checking what you're doing and determine whether there is a better way to implement the type of testing you're doing. It's easy to get carried away when applying new techniques, but it's often the case that a more verbose but familiar pattern is a better choice.