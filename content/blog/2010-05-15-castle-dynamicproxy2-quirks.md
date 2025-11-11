---
id: 552
title: Castle DynamicProxy2 quirks
date: 2010-05-15T15:35:31+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=552
#permalink: /?p=552
tags:
  - 'c#'
  - gotchas
  - patterns
  - software
  - castle-dynamic-proxy
  - aop
  - advice
---
I've been faffing around with [Castle.DynamicProxy2](http://www.castleproject.org/dynamicproxy/index.html) a bit lately and it's a pretty interesting bit of kit. Castle Dynamic Proxy (CDP) allows you to dynamically generate proxies at runtime to weave aspects of behaviour into existing types. Aspect oriented programming is typically employed for implementing crosscutting concerns such as logging, performance measuring, raising INotifyPropertyChanged and various other types of repetitive and/or orthogonal concerns. I'm a newbie to this stuff so I won't say much more on AOP.

While I really like CDP, I've found that the documentation and tutorials (the best of which is <span>Krzysztof Koźmic</span>'s excellent [tutorial series](http://kozmic.pl/archive/2009/04/27/castle-dynamic-proxy-tutorial.aspx)) aren't particularly explicit on **how** CDP achieves its effects, and sometimes these details are important.

There are two main ways of creating proxies that most developers will encounter.

### CreateClassProxy

This is nearly always the first demonstrated method in tutorials. [ProxyGenerator.CreateClassProxy](http://api.castleproject.org/html/Overload_Castle_DynamicProxy_ProxyGenerator_CreateClassProxy.htm) dynamically subclasses the target class, so if you have a class named Pogo and you call ProxyGenerator.CreateClassProxy, what you'll get back is an instance of a _subclass_ of Pogo (i.e. the new type _is-a_ Pogo) that weaves in the interception behaviour via overriding methods. This is why it is a stipulation that methods / properties must be virtual when they're intercepted.

With class based interceptors, you cannot intercept non virtual methods because unlike Java, C# does not make methods virtual by default. If you try to intercept a non-virtual method, nothing will happen, though mechanisms do exist to allow you to identify these situations and warn the developer (the most common example of this is that NHibernate will die on its arse if you try to use lazy loading with a non-virtual member).

### CreateInterfaceProxyWithTarget

The second method is [ProxyGenerator.CreateInterfaceProxyWithTarget](http://api.castleproject.org/html/Overload_Castle_DynamicProxy_ProxyGenerator_CreateInterfaceProxyWithTarget.htm), and it is the primary reason for writing this blog post! CreateInterfaceProxyWithTarget does not dynamically subclass target types, it simply creates a dynamically generated class, implements the same target interface and then passes through to it. I.e. it's an implementation of the [decorator pattern](http://en.wikipedia.org/wiki/Decorator_pattern). This has two effects, one of which is very important!

1. You don't need to mark your methods/properties as virtual
2. Since it is a proxy working via decoration rather than subclassing, for the effects of the interceptor to be applied, all calls must be made **on the proxy instance**. Think about it.

The most salient point is #2. I'll elaborate.

### A worked example: Rocky Balboa

Say you have an interface called IBoxer like this:

<img class="alignnone" src="images/iboxer.png" alt="" width="213" height="124" /> 

... and you implement it like this:

<img class="alignnone" src="images/rocky.png" alt="" width="473" height="384" /> 

If you then turn to aspect oriented programming and decide to gather statistics on punches thrown for the duration of a boxing round, it's a reasonable assumption that you can simply proxy the IBoxer interface and intercept only the StraightLeft/StraightRight punch calls, tally them up and report the metrics (ignore whether this is a good idea to be doing this, it's a contrived example). On the face of it this isn't a horrible idea. However, it won't work as expected.

The key here is that OneTwo() calls through to StraightLeft() and StraightRight(). Once the proxy has delegated to the decorated type it loses the ability to intercept the calls. We can follow the call graph easily enough. We have a reference to the proxy via the IBoxer interface. We call "OneTwo()" on it and when the invocation proceeds, it delegates to the decorated Rocky instance. The Rocky instance then calls StraightLeft(), StraightRight(). Both of these calls will immediately go straight to the 'real' implementation, bypassing the proxy.

Just as with the normal decorator pattern, the decorator (the IBoxer dynamic proxy in this case) loses its influence when the decorated object calls methods declared in its own public interface. In this particular situation we could write an interceptor that knows to add two punches when OneTwo() is called on the proxy, but compare this approach to one using class based proxy. If we were using a class proxy we could rest safe in the knowledge that all calls to StraightLeft() and StraightRight() will always be intercepted, as the extra stuff we've bolted on resides in a method override.

The results vary depending on the type of proxy we generate and the way the types are written. In hindsight it's pretty obvious, but it still caught me out.