---
id: 407
title: "Internals: To test, or not to test?"
date: 2009-10-09T01:01:06+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=407
#permalink: /?p=407
tags:
  - testing
---
Prepare for some flimsy and strange analogies.

I've been reading a few stackoverflow questions dealing with whether you should test the guts of a system as well as the public API. Most of the people who advocated never testing anything but the main class APIs seemed to talk as if these APIs were extremely coarse-grained and any change to the internals would result in major breaking changes to the tests. This strikes me as somewhat strange, as it's often not the case in my (admittedly limited) experience.

On the other hand, many of the developers who advocated testing the implementation details also advocated test-driven development (TDD); that's when the penny dropped. To me, this is a good illustration of why designing for testability can make change less painful. Sometimes I cringe when I hear the phrase "agile" bandied about, but it rings true here.

### Little, bitty pieces

Designing for testability in conjunction with TDD tends to produce loosely coupled classes that have very few responsibilities. You trade more complicated wiring and interactions for unit isolation and simplicity. In the majority of cases, I feel it is an attractive proposition. Instead of one 3000 line class that does everything, I end up with 25 x 50 line classes and the odd bigger one here and there.

Complicated behaviour is usually achieved through composition (inversion of control using constructor injection) and delegation. I consider most of my inner classes to be implementation details, because the user doesn't get to do anything with them. They're off sitting in a library somewhere; they're not exposed to the user. The user gets a hold of the top level class that tells the innards to do the real work (instead of the 3k line class that does _everything_). I can take any unit in the system off the shelf and test it without a struggle.

So, who is going to suffer more breaking changes and hardship if they test the internals? Is it the developer who writes the all-singing, all-dancing monolithic class, or the developer who writes numerous, small, simple classes that can easily be tested in isolation without any fuss? Since you're reading a testing blog, I think you know what I'm going to say, and it's not going to be the twisted brain-wrong of a one-off man mental*.

### Big is awkward

Large classes are harder to understand, maintain, refactor and test thoroughly. Furthermore, it is my experience that the biggest classes tend to grow and grow. The bigger it grows, the more ungainly it becomes. Gangly limbs poke out every side; sharp edges are present in abundance. It'll probably stick the heid on you or [punch you into paralysis](http://www.imdb.com/character/ch0029856/quotes).

Have you ever picked up a huge class and been tasked with adding new functionality and testing it while you go? It's painful. By the time you've worked out which tightrope you've got to walk (and fallen off it 20 times due to the principle of _most_ surprise), you've wasted a lot of time adding in the new functionality and even more time writing the tests.

### Small is beautiful

Contrast that to a system where you just add a method or two in a simple class (or add a new one) and the maintenance headache is reduced to a dull ache. If it's easy to write, it's easier to understand, test, maintain, refactor and - just as importantly - **it's even easier to throw away**. I don't get attached to tiny classes or their respective unit tests. They're like tic-tacs; if I lose one or five, I shrug. Big deal. I get some new ones. Open for delete. Don't cry you buffoon, it's just a tic tac.

Misko Hevery recently [posted something interesting](http://misko.hevery.com/2009/10/01/cost-of-testing/) on his testing breakdown and, while most of us won't reach his level of testing efficiency, it's an interesting read. Misko states that the vast majority of his time is spent writing production code, **not** test code. Yes, the ratio of lines of test and production code produced is almost 1:1, but the time invested is wildly different. Test code is usually verbose, but it's easy to write out when your classes are small and you test in lockstep.

In summary, I believe testing the guts of your classes can be a worthwhile approach, but designing for testability is paramount when doing so.

[*](http://www.imdb.com/character/ch0017429/quotes)