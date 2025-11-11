---
id: 22
title: Why write test code?
date: 2009-03-07T14:10:41+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=22
#permalink: /?p=22
tags:
  - testing
---
It's not uncommon to encounter developers that are wholly resistant to unit/functional/integration testing. Some of them will simply dismiss the idea due to thinking it's new-fangled rubbish ("I never unit test, and my code is fine"). Other developers may recognise the positive impact tests can have, but simply deplore spending any time writing them. Some folk will go to great lengths to either bypass the test writing stage, or write tests in a fashion that gives zero or even negative returns!

So, why should we write tests? At a very high level, the answer is simple: If the tests are well-written, **automated testing helps prove that your software works**. I'm the first person to admit that automated testing is not a silver bullet, but particularly with state-based testing, it can be extremely effective at verifying that **your code does what you think it does**. What you _think_ your code does and what it _actually_ does are two entirely separate things.

To try to bring some of the test-sceptics on board, I will ask a simple question: What do you do when writing a fairly complicated algorithm that can be verified by looking at the values/output/state?

If you're anything like me, you draw/write the desired result and then try to come up with an algorithm that satisfies all of the required conditions. For example, for a terrain grid algorithm, I would draw a grid with the vertices, edges, indices and so on. I'd then iteratively write an algorithm that generates terrain, testing its output values using pencil & paper. When the algorithm finally satisfied all of the conditions I'd set, it'd be fairly robust. To be sure it works for numerous inputs, I'd then draw a few more examples and double check that the algorithm can produce the result for multiple cases (e.g. 3×3 tile, 1×5 tile, 2×2 tile). Can you see the parallels? Each set of desired results/values is a test case.

I hope you can see what I'm getting at: **Pencil & paper testing is a form of test-driven development**. The main difference is that the pencil and paper tests go back in the drawer never to be seen again, but the automated tests remain. In addition to ensuring that the code does not regress, they provide a form of documentation and are a great aid when refactoring & optimising. Furthermore, at this stage, it is generally easier to write new code tests, meaning you can cover more edge cases without having to sharpen the ol' pencil again.

If you've ever followed the pencil and paper process, you have been testing without knowing it. Other than my own endeavours, I have personally witnessed software engineers transferring their pencil & paper tests into unit tests and then creating scores of test variants. The result? Numerous bugs were found and the time spent testing proved to be hugely valuable.