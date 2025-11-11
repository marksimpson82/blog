---
id: 675
title: "Functional-style programming - Easy debugging!"
date: 2012-07-07T21:34:15+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=675
#permalink: /?p=675
tags:
  - 'c#'
  - debugging
  - MyWorld
  - patterns
  - software
  - tips
---
Ever since LINQ arrived in C# land, a lot of people have been using a functional style of programming without even perhaps being conscious of it. 

I always chuckle when I read the words "functional style", because I picture grim marches across a barren landscape, brutalist architecture and people with beards. 

One particular facet of programming in a functional style is where, rather than mutating an existing piece of data, input data is transformed / projected into something new via a [pure function](http://en.wikipedia.org/wiki/Pure_function). Since this style of programming limits the number of side-effects, it makes debugging a comparatively wonderful experience. 

## The status quo

First, let’s consider business-as-usual. Imagine you’re debugging a part of your program that is doing something complicated. The program is written in the usual imperative, OO style; that is to say, when method calls occur, state is mutated.

It’s often the case that an object with state either mutates itself, or is mutated by other objects. Once that code has been executed, the old object state is gone. It’s done one. It ain’t comin’ back, Billy. When you observe the result and see a problem, the data trail goes cold. All you can see is the state of the object _after_ it has been mutated. Sometimes you can work your way backwards, but in other cases the mental gymnastics are too complicated. Sometimes you weep hot salty tears.

To reproduce the bug, you need to get the program back into its original state and observe proceedings as they happen. This can be tricky, especially when the reproduction steps are unknown.

## Step forward, functional style

If you’re simply transforming some data D by some function F, you get something like `F(D) = D’`. 

`D’` is a new object or structure. The original input data `D` remains untouched. If your program is incorrect after the transformation, all of the original state still exists. 

You can simply break in the VS debugger then use the “Set Next Statement” to rewind the execution to an arbitrary point. As long as the operations have no side effects, you can do this as many times as you want or to any depth. It’s almost like you recorded the drama on tape and rewound it.

## Stuff wot I’m doing

The current program I’m working on is developed using a series of stages. It goes something like this:

“Take this raw json input, build a graph. Take the graph, build a higher level representation with bells on. Take the higher level representation with bells on, build a triangle mesh with texture coordinates.”

At pretty much every stage, I am transforming input data into something new rather than mutating an existing structure. There is precisely one part where I mutate data. Guess where I spent the most time debugging it when unexpected input data caused it to crash? Yup, the mutation bit. 

We have terabytes of data to crunch. It is vital to be able to reproduce crashes in a deterministic fashion.

I’m not claiming this style of programming is a silver bullet or applicable everywhere, but it does have its charms.