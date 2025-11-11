---
id: 847
title: Nvidia + G-SYNC - Black screen when alt-tabbing
date: 2020-03-29T21:14:28+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=847
#permalink: /?p=847
tags:
  - nvidia
  - g-sync
  - black-screen
  - bugs
  - tips
---
**tl;dr:** It seems G-SYNC related. I fixed it by installing the monitor driver, then toggling G-SYNC on/off. 

**The problem**

I've had an irritating PC problem for a few months, hopefully this post helps folk with the same problem. 

When entering/exiting full-screen video or alt-tabbing out of a game, the screen would go black for a few seconds - it was pretty sluggish, too. 

It's one of those issues where finding the right search terms took a while, and it tended to turn up irrelevant posts from years ago, or similar problems with solutions that no longer apply (e.g. "set X option in the driver" where X option no longer even exists).

**My PC**

  * Windows 10 Home Premium, 64 bit 
  * NVIDIA 1060 Ti 3GB (driver version: 442.59)
  * Benq XL2540 

**The solution**

First, I installed the monitor driver for my XL2540 (I never install monitor drivers, but I needed to do this or the GSync option failed to show up in the Nvidia Control Panel). 

Then, I toggled G-Sync on, then back off. Detailed instructions:

* Open Nvidia Control Panel: 
* Click "Display > Set up G-SYNC" 
* Under the "1. Apply the following changes" text
* Check the box named, "Enable G-SYNC, G-SYNC Compatible"
* Click "Apply" (the screen should go black, then confirm everything is OK) 
* Uncheck the same box ("Enable G-SYNC, G-SYNC Compatible")
* Click "Apply" and confirm once again.

Thanks to Ethan Snider for his [comment](https://www.youtube.com/watch?v=m0T0Oln6khk&lc=UgwnxpFEgo8lJnkTDHZ4AaABAg) on a youtube video for pointing me in the right direction.