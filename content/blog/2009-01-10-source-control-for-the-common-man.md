---
id: 14
title: Source control for the common man
date: 2009-01-10T23:28:31+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=14
#permalink: /?p=14
tags:
  - Uncategorized
---
Due to barely taking a day off during my first six months (my own choice), I accrued so many unused holidays that I found myself with a stretch of 17 or 18 days of holiday over Christmas. Now, I've never been one to shy away from laying around for prolonged periods, but this time around I found myself restless after a week or so. In the end, I cracked; I started programming quite a bit - just pottering around doing my own personal experiments.

It was fun, but I realised that developing at home wasn't quite as fulfilling as it is at work. I have a good PC at home, dual screens etc. so it wasn't that -- it was something that never used to bother me: a lack of [source control](http://en.wikipedia.org/wiki/Source_control). I kept finding myself in situations where I wanted to undo something, but I'd closed the file and/or forgotten to back something up before making a change. When you're used to using source control every day, its absence is painful. Now, this will likely result in me being labelled as a heathen by some (Hi, Mishets :P) but I really couldn't be bothered downloading and setting up [SVN](http://subversion.tigris.org/). I've used [SVN](http://subversion.tigris.org/) before and it worked fine, but I use perforce at work, so perforce was the ideal solution.

Handily, perforce offers a free server and client download for up to two users. For personal work, this is perfect. The reason I'm posting about it is because it was incredibly easy to set up - I was impressed at how simple the process was. The client and server are tiny downloads, the configuration (for my needs anyway) was cursory and the results immediate. Although Perforce can be a little cranky at times, I think it's well worth a look.

Additionally, if you get a job programming (or doing anything related to programming) source control software is almost definitely going to be involved, so it pays to start now and get used to it. While some will scoff and say "well, obviously!", I will qualify in advance by saying that some programmers don't use source control software prior to filling in job applications; some don't even know what it is!

[The perforce download page has the server & P4V client files](http://www.perforce.com/perforce/downloads/index.html)