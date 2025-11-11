---
id: 654
title: The Power of Boy Scouting & Git Stash
date: 2012-04-16T02:04:00+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=654
#permalink: /?p=654
tags:
  - whinges
  - software
  - tips
  - git
  - git-stash
---
No, I’m not advocating beavering your way to several badges while wearing ill-fitting shorts, a neckerchief fastened with a woggle and risking a criminal record. I’m talking about [The Boy Scout Rule](http://programmer.97things.oreilly.com/wiki/index.php/The_Boy_Scout_Rule). 

The gist of it:

> The Boy Scouts have a rule: "Always leave the campground cleaner than you found it." If you find a mess on the ground, you clean it up regardless of who might have made the mess. You intentionally improve the environment for the next group of campers. Actually the original form of that rule, written by Robert Stephenson Smyth Baden-Powell, the father of scouting, was "Try and leave this world a little better than you found it." 
 
What if we followed a similar rule in our code: **"Always check a module in cleaner than when you checked it out."** No matter who the original author was, what if we always made some effort, no matter how small, to improve the module. What would be the result? 

## Why it matters

As a programmer, sometimes it’s doing the little things that makes everybody’s collective life a little bit easier. There’s a lot written about the practical benefits of doing this (namely: the ability to continually deliver without having to scrabble around in a dung-heap, weeping with shame) but, for my money, the most important thing is that it makes writing code more enjoyable on a day to day basis. 

I always get irritated and furrow my brow when I find code that has been allowed to drift. When you think of the amount of times you run into a bewildering part of a codebase and spend 10 minutes scratching your head because something has a misleading name or there’s some dead code confusing the issue, why not just fix it up? Fine, you’ll probably have to spend a 5 to 10 minutes making the change (less with lovely refactoring tools like [ReSharper](http://www.jetbrains.com/resharper/)), but code is write once, read many. Code hardens like cement, so there’s no time like the present.

The mechanical process of Typing Shit and Testing your Changes usually takes little to no time at all. If you save a few people the same 10 minutes of teeth-gnashing frustration, then you have made a positive change. 

## Context Switching

It’s often the case that I’m midway through feature work and don’t want to refactor as part of the same changeset, but nor do I want to submit my WIP changes. Refactoring is meant to change the structure of the code, but leave the functionality intact; refactoring and changing the function of the code in the same submission is often asking for trouble. Nobody wants to be the guy that broke something while ‘improving’ the code. Broken is not better.

In the past, I used to note down the thing that was irking me and fully intend to fix it up later, but I’d often forget to do it or be unwilling to spend the time re-acquainting myself with the problem when I returned.

Nowadays, I’m trying to Just Do It. It’s 2012 folks. The tooling exists to make this work.

### Perforce

I’ve used perforce extensively. Perforce [introduced shelving](http://www.perforce.com/perforce/doc.current/manuals/cmdref/shelve.html) a while back. In short, shelving allows you to store your WIP changelist on the P4 server without it being a bona-fida commit. You can use this for storing WIP changelists and reverting them locally. This allows you to jump onto something else without committing changes beforehand. Handy. 

Even more handy is that anyone can un-shelve your shelved changelists. 

### Git

Git is a really cool bit of kit. Caveat Emptor: I’m not sure if it’ll shit the bed in asset-heavy projects, but we’re using it at work for our Mapply codebase and it’s a lovely change of pace. It took me a while to get to grips with the many-branches-but-only-one-location-on-disk thing, but it really is amazing. The reason I say it’s amazing because it allows me to work in different ways to traditional client/server SCM.

With Git, if you create a local feature branch for every single thing you work on, you’re pretty much 90% of the way there. 

If you don’t want want to commit your work in progress changes before starting work on the distraction, you can simply use [Git Stash](http://book.git-scm.com/4_stashing.html) instead. Git stash pushes your work in progress changes onto a local stack for safe-keeping. Once the stash command has been issued, you’re back to a clean state and ready to work on something else. At any point in the future, you can resume where you left off by typing git stash pop.

This makes it incredibly simple to hop around and fix up whatever the hell is annoying you at any given moment without polluting a changeset with unrelated fixes. 

Happy scouting.