---
id: 810
title: "Focused commits (also: git add -p)"
date: 2018-04-06T00:10:28+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=810
#permalink: /?p=810
tags:
  - git
  - tips
  - vcs
---
Many people use version control as a bucket for their stuff. They commit and merge in some shape or form, and it gets shared with their colleagues. Everyone moves on with their lives. Fire & forget sucks when using distributed version control systems.

The trouble with this approach is that it gets complicated to track two simple things:

  1. When was a change introduced?
  2. What is the purpose of the change?

How do we use git in a way that makes it easy to track both _when_ a change was introduced, and the _intent_ of the change?

## The when

The first point (the what) has been written about a lot. The gist of the workflow I use is that constantly rebasing when pulling, and squashing any merges on their way back to master helps a great deal.

I.e. when you're working on a feature branch and have local commits that haven't been pushed, use the following to avoid noisy merge commits:

`git pull origin mybranch --rebase`

To keep your own (non-shared) branch up to date with master, but without creating merge commits, periodically do something like:

```bash
git pull origin master
git checkout mybranch
git rebase master
```

(Small tip: if you are pushing your own personal branch after rebasing, you can be sure not to nuke anything important by employing [git push -force-with-lease](https://developer.atlassian.com/blog/2015/04/force-with-lease/) rather than git push -force).

Then when you're ready to merge back to master:``

```bash
git checkout master
git merge mybranch --squash
git commit
```

There are many advantages:

* It keeps the history linear
* There's no merge noise
* It groups related commits
* Reverting a feature merge is easy (i.e. you can just revert the squashed merge)
* The default commit message will contain the hashes for all squashed commits, so fine-grained operations & the intent for all of these changes are still there.
* ... and arguably best of all, you can trivially figure out which commits introduced bugs when QA says, "hey, CI build 1923's frob widget is misbehaving" (when commits are interleaved from a long-running branch, the offending commit may actually show up in the history as being months old).

The only time I deviate from this pattern is when I'm suffering a lot of merge pain - standard rebasing means merging up your _individual_ commits, so it can mean a lot of repeated work needs to be done in areas where merge conflicts frequently occur. You can interactively rebase & squash your branch's commits to reduce the number of commits that require merging or use [git rerere](https://git-scm.com/docs/git-rerere), but it's fairly complicated vs. the usual workflow.

## The why

OK, so that's the when taken care of. What about the _intent_ behind the code, or a particular commit? This one's even easier to solve, it just requires some better commit discipline.

#### Committing a crime

Here's a quick scenario: A developer, Eddie, has been tasked with improving the performance of an application. Eddie profiles the code and figures out some areas they think need improvements. They make the changes, profile the app and find it's now 20% faster. Great! Oh, and they also reformatted some source files, made a number of variable names compliant with the company's coding standards, upversioned a header-only library, refactored some code_and_ added a few missing pieces of dev functionality that made the app easier to work with for profiling.

All told, 45 files have been touched, and 5000 lines of code changed (mainly due to the formatting and library churn). All of these changes are made in one commit, with the a message saying "improving performance of app".

Four months later, a few bugs are discovered in a seemingly unrelated area of the app, and are traced back to this commit. Another programmer, Irene, is tasked with fixing it.

#### Playing detective

Irene loads up the offending commit on github, and immediately gets irked when she spots the "change too large to display" message. At this point, Irene's day is much worse than it should've been.

Was it the formatting changes? I mean, it's unlikely, but sometimes people make changes by hand and fat-finger a key or transpose something important. The simplest changes can be the most dangerous (think of the number of [ya, yb, yc, xw] errors static analysis tools find...)

Was it the refactoring? It touched a lot of files. Hard to say without reading the code or just reverting them, then re-applying the other changes.

Was it the library upgrade? Again, hard to say. Even if it is, the commit message didn't say if the new version was added for performance reasons, so perhaps Irene will need to re-profile the app to be sure.

Was it the new functionality? ... and so on. It's really annoying.

#### Better commit(s)

VCS commits are like code - written once and read thousands of times later (especially in complicated, high-traffic areas of code). They can be precise and explain the background behind the change, or they can be unfocused while burying the reason for making the change in the first place.

While we're all busy (yes, I make numerous lapses of judgement, too...), there are simple ways you can try to be a good citizen.

Firstly, make your commits as concise as possible. If fixing a bug requires changing precisely two lines, then please change those lines, _but nothing more._ If your bugfix isn't resolving all instances of the problem, the next programmer that picks it up has two lines to start pondering. Two! Not 5000. Huge difference.

Secondly, make your commit messages as thoughtful as possible. By this I mean "how can I make the reader understand the change I've just made, as well as the context?" There are numerous things to talk about. Off the top of my head:

  * Why is the change being made?
  * How does it work?
  * If it's a complicated change, can you describe the program's state and how this change helps?
  * Are there any caveats?
  * Where did the solution come from, is there any prior art?
  * Why solve it in this particular way when <other way> seems more appropriate?
  * Is anything else suffering from the same problem?
  * Is it a hack that needs to be properly fixed in future?
  * Can the change be reverted when library X we're using ships a fix instead?
  * Are there any bug numbers or related commits worth referencing?

Thirdly, as an addendum to #1: do not include orthogonal changes in a single commit! If you want to change the formatting of a file please do so, but not while also changing its functionality, fixing a bug and adding a feature. Do one, then the others later.

#### git add -p

If you find yourself noodling away like I do ("ooh, I'll just refactor this while I'm here"), it's easy to find yourself in a situation where you want to make a focused bugfix commit, but the file also has unrelated formatting changes. With a bit of practice, you can use git add -p. The patch (-p) flag allows you to recursively split the file, then stage sections of it. You can then pick and choose which parts to stage & commit! Great.

Certain IDEs also have VCS integration where you can select the hunks to stage, too.

Nothing's ever free, so when using patch mode, take care that your changes don't mix & match too much, or you may accidentally take part of change A and roll it in with change B (e.g. you renamed a variable, and failed to notice it crept into a prior commit).

If you're making large changes, it's better to just do the work later.