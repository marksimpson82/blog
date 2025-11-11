---
id: 421
title: Is your test code readable?
date: 2009-10-26T01:31:05+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=421
#permalink: /?p=421
tags:
  - testing
  - tips
---
One of the things that _really_ slashes the return on investment in testing is unreadable code. "This is pretty obvious", you say. "What's the point in a blog post about something so obvious?" What's not obvious is that the very people writing these tests are unaware of it. Maybe you do it as well. Given that this blog post is about _things we don't know we do_, I think it's a fair bet that I've also recently written test code that was convoluted without realising it, too.

It's mostly down to testing in a vacuum. The tests are often functionally fine. However, as with nearly all code, maintenance is easily overlooked. On the day that the test was written, it made sense to the author. They understood the logic they wanted to test and how to implement it. Code written, job done.

### In the court of the test engineer, readability is king

In my opinion, readability in tests is the **number one** thing. If your fellow programmers and your future self cannot decipher what a test is proving, the test becomes worthless. If a monstrously bearded mathematics genius solved solved [P versus NP](http://en.wikipedia.org/wiki/P_%3D_NP_problem) but failed to write an understandable proof, it would all be for nothing.

It's the same for testing. You'll know the shit has hit the fan when you're refactoring something and break a load of tests. "Balls. I'll fix the tests I guess", you murmur, bleary eyed and idiot-faced. However, when you examine the tests, you can't figure out what they're proving, why they're proving it or how it's actually proved!

You know in films when a bad guy is holding a hand grenade, then has a moment of realisation regarding an absent pin? He slowly looks up, face furnished with a quizzical look, staring into oblivion. That's what a software engineer looks like when they encounter reams of broken tests that cannot be deciphered (and the person who wrote 'em isn't available to pick up the pieces).

### Grab a friend and test your tests

To avoid these kinds of bomb-scares, do yourself a favour and have somebody else trawl through your test code _without giving them any help_. If they cannot easily follow the test code's intent, then the test needs re-written. Everybody's code can be improved through peer review. Peer review is the litmus test - if somebody else cannot understand it, it's useless. As such, tests should be part of code reviews and buddy processes.

Think about how much time we spend reading, maintaining, refactoring and extending _old code_ compared to writing new code, and then think about how self-defeating it is to write unreadable, un-reviewed test code. Spending a little more time on reviewing new test code pays off in the long run.