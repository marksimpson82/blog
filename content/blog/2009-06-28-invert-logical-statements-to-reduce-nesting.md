---
id: 357
title: Invert logical statements to reduce nesting
date: 2009-06-28T18:32:31+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=357
#permalink: /?p=357
tags:
  - 'c#'
  - software
---
As a test engineer, I spend a lot of my time reading -and making sense of- other people's code. I find it interesting that logically equivalent, re-arranged code can be much more easily understood. Some of this follows on from the layout / style guide in the excellent [Code Complete](http://www.cc2e.com/ "code complete 2"). Perhaps I have unknowingly assimilated these idioms from reading, understanding and ultimately copying the layout of 'good' code. Either way, they're useful from a testing point of view, as it's simpler to reason about code that doesn't jump around so much.

As has been stated many times before, in general, the best programmers are the ones who program around the limitations of the human brain. E.g. splitting a method into self documented sub methods, reducing nesting depth, reducing number of exits from a loop, grouping related logical statements and so forth.

Along similar lines, here's a very simple but effective one: something I like to call "_flattening_".

### Reduce nesting by inverting logical statements

It's a fairly simple concept. By flipping a logical test or statement, you change the layout of the code, but the result remains the same. Compare the two following two snippets:

**Approach One**

```cs
if(someval != null) 
{
  if(someOtherVal != null)
  {
    if(anotherVal == 10)
    {
       if(someOtherCondition)
       {
           DoExtraStuff();
       }
    }
 }
```

**Approach Two**
```cs
if(someval == null)
  return;

if(someOtherVal == null)
  return;

if(anotherVal != 10)
  return;

if(!someOtherCondition)
  return;
       
DoExtraStuff();       
```

Even with these trivial examples, I think the first one is much more convoluted and harder to follow. If invariants must hold at the start of a method, it makes much more sense to check them and return / return an error / throw an exception (as appropriate). If multiple nested if statements are used from the start, the nesting depth in the method is increased by default. Any further indentations compound the problem and reduce clarity.

I've seen fairly large methods (multiple pages) that suffered from this kind of problem and it made the code much harder to follow, especially when non-trivial work was done towards the end or a value was set earlier and returned later. By the time you scroll to the end to deal with the problems, you've forgotten what came before.

By contrast, the second method is much flatter. It basically reads like: "if this is invalid, return. Done. If the other one is invalid, return. Done. OK, we have valid inputs, so forget the validation phase and get started with the real work". It's like removing a couple of juggling balls from the air - it removes a mental burden because you can simply ignore the initial checking logic.

You can also do things like introduce the _continue_ keyword in loops and a few other things, but there are often caveats associated with such choices.

I use 'flattening' it in a lot of places, but there are occasions when it doesn't make sense to flatten a method. Sometimes it's nicer to deal with the 'standard' case first regardless of the extra nesting depth. In other scenarios, you can reduce nesting through the use of the continue keyword in loops, but lobbing a 'continue' keyword half way into a loop body adds a different _kind_ of complexity, even if it means reduced nesting depth.

I.e. I like to use this a lot but, like most things, it shouldn't be used indiscriminately.