---
id: 467
title: Debug.Assert vs. Exceptions
date: 2010-01-09T18:53:30+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=467
#permalink: /?p=467
tags:
  - testing
  - software
  - asserts
  - exceptions
---
_"When should I use Debug.Assert and when should I use exceptions?"_ - It's a fairly sensible question to ask, but you've got to sift through a lot of articles to get anything resembling solid guidance on it (<a href="http://stackoverflow.com/questions/1467568/debug-assert-vs-exception-throwing/1468385#1468385">Eric Lippert's stack overflow post is particularly enlightening</a>). I've wrestled with it quite a bit as a programmer and test engineer, so here's my 2 pence.

## Good rules of thumb I've arrived at
1. Asserts are not a replacement for robust code that functions correctly independent of configuration. They are complementary debugging aids.

1. Asserts should never be tripped during a unit test run, even when feeding in invalid values or testing error conditions. The code should anticipate and handle these conditions without an assert occurring!

1. If an assert trips (either in a unit test or during normal application usage), the class containing the assert is the prime suspect, as it has somehow managed to get into an invalid state (i.e. it's bugged).
  
For all other errors - typically down to environment (network connection lost) or misuse (caller passed a null value) - it's much nicer and more understandable to use hard checks & exceptions. If an exception occurs, the caller knows it's likely their fault. This is what makes the .NET base class libraries a joy to develop with - it usually clear when you are misusing an API, resulting in fewer <a href="http://www.pragprog.com/the-pragmatic-programmer/extracts/tips">"select is broken"</a> moments. It fails early and clearly communicates the reason for failure.

You should be able to test and use your class with erroneous input, bad state, invalid order of operations and any other conceivable error condition and an assert should <strong>never</strong> trip expectedly. 

Each assert is checking something should <strong>always</strong> be true regardless of the inputs or computations performed. If something should always be true, then the number of asserts used shouldn't be a barrier to thorough unit testing. If an assert occurs, the caller knows it's likely a bug in the code where the assert is located.

If you stick to this level of separation, things are a bit easier.