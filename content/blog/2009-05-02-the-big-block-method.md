---
id: 238
title: The big block method (binary search)
date: 2009-05-02T17:28:28+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=238
#permalink: /?p=238
tags:
  - 'c#'
  - debugging
  - testing
---
Have you ever been in this situation? You have thousands of tests in scores of assemblies. All of the tests pass. However, when you run the test suite a second time without closing NUnit (or your test runner of choice) you find hundreds of failures occur in a specific area. I'm not talking about in the same fixture or even the same assembly; this is NUnit wide. Something is trashing the environment, but there are no obvious warning signs.

So, we have thousands of tests - the problem could be anywhere. The answer is obviously not "look through all the tests" or "disable one project at a time", there has to be an easier way...

### Unrelated, but applicable

This just happened to me, but tracking down the culprit wasn't as bad as you'd think.

Something I learned as a budding level designer (circa ~1999) was how to find a leak in my level. A leak in level design occurs when the world is not sealed from the void. A decent analogy is to imagine the inside of the level is a submarine and the walls are the 'hull' - if there is a gap anywhere in the hull the water will get in; it will leak.

A leak could be something as tiny and obscure as a 1 unit gap between a wall and a floor. Most walls are 128 to 256 units, so a 1 unit gap is very small. Even now, it's not really feasible to find one in the editor unless you know exactly where it is.

Half-Life's goldsrc engine was BSP based; the visibility computations were performed at map compile time. A failure to build VIS data meant that your level caused the game to run at about 3 frames per second.

Unfortunately, tools were really ... rudimentary back then. These days pretty much every editor has built in pointfile loading (meaning it will take you directly to the leak!) but back then, you had to be creative.

### The big block method

Back when tools weren't so great, to find leaks in a level, I used the big block method. It's a very simple technique. Say we have a rubbish, leaky level like so (top down view):

<div style="width: 363px" class="wp-caption alignnone">
  <img title="Big block" src="https://defragdev.com/blog/images/bigBlockProblem.png" alt="A level, yesterday." width="353" height="289" />
  
  <p class="wp-caption-text">
    A leaky level, yesterday.
  </p>
</div>

If one of those connections between walls/floors/ceilings/whatever is not tight, it will leak. We cannot see the site of the leak using our eyes. We cannot be sure where the leak is by simply scrutinising each wall joint or entity. What we can do instead, though, is place a big block over ~50% of the level.

<div style="width: 363px" class="wp-caption alignnone">
  <img title="50% of the map is now covered" src="https://defragdev.com/blog/images/bigBlockStep1.png" alt="50% of the map is now covered" width="353" height="289" />
  
  <p class="wp-caption-text">
    The red area is a newly created solid block
  </p>
</div>

If we compile and find that the leak has disappeared, we know that the leak was definitely in the area that is now covered by the block. On the other hand, if the leak is still present, it's in the other 50% of the level that remains uncovered. To hone in on the problem area, all we have to do is recursively add blocks to the problem area:

<div style="width: 363px" class="wp-caption alignnone">
  <img title="Recursively adding blocks half the size of the previous block..." src="https://defragdev.com/blog/images/bigBlockStep2.png" alt="Recursively adding blocks half the size of the previous block..." width="353" height="289" />
  
  <p class="wp-caption-text">
    A smaller block has been added
  </p>
</div>

We then recompile and check to see if the leak has disappeared as before. Notice that in **two** steps, we've narrowed down the problem's location to an area of **25%** of the original size! The next step will yield a further 12.5% reduction. We quickly hone in on the problem.

After I started programming, I realised that the leak-finding method I used as a level designer is a simple [binary search](http://en.wikipedia.org/wiki/Binary_search_algorithm).

### Same thing, different discipline

Applying the same principle to finding problem tests or code is simple! Divide and conquer.

Open the NUnit test project file and remove 50% of the projects (though in my case, I kept the assembly with the tests that failed, as I needed to see them fail on the second run to know the problem had occurred). Run the tests twice to see if the failure occurs on repeated runs. If they fail, you know your problem is in that group of assemblies. If they pass, you know the problem is in the other half.

It's then a case of whittling it down in the same way - disable a further 25% of your assemblies, run the tests twice and check the result. Rinse, repeat.

Eventually you will (most likely!) be down to two assemblies - the assembly that exposes the problem and the problem itself. If there's a large amount of tests and fixtures in the assembly you're scrutinising, disable half of the fixtures and repeat the process. You will rapidly converge on a fixture and, finally, the test that causes the problem. From then on it, it's just standard debugging.

In my case, the culprit ended up being a single line of code calling into a method that has been a long-standing part of our code base. It looks totally innocuous, and there is absolutely no way I'd have found so quickly without dividing and conquering.

From the top level, with scores of assemblies and thousands of tests, it may as well be a 1 unit gap.