---
id: 642
title: Gigabyte GeForce GTX 560 Ti OC - Avoid
date: 2011-12-01T02:34:45+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=642
#permalink: /?p=642
tags:
  - misc
  - whinges
  - tips
---
[This card](http://www.google.co.uk/products/catalog?hl=en&safe=off&q=gigabyte+geforce+gtx+560ti+oc&gs_upl=336l603l1l704l3l1l0l1l1l0l95l95l1l2l0&bav=on.2,or.r_gc.r_pw.r_cp.,cf.osb&biw=1920&bih=1096&um=1&ie=UTF-8&tbm=shop&cid=1323606381779257544&sa=X&ei=iOHWTrGKA9Gg8gP8vL3rDQ&ved=0CDIQ8wIwAA), amongst various other factory overclocked GTX 560 Tis are [causing problems](http://forums.whirlpool.net.au/archive/1639211) for lots of people. There are various 560 Ti cards that have the OC postfix which stands for “Overclocked”, but the Gigabyte one seems to be the biggest offender.

# tl;dr summary:

<font color="#ff0000" size="4">Batches of these cards do not run at their advertised speeds with certain DX11 games. The cards are either stretched beyond their comfort zones, or don’t get enough voltage.</font>

<font color="#ff0000" size="4">If you have one of the unreliable cards and play the likes of Crysis 2 or Battlefield 3, your game will probably crash with a silent error, or a driver error.</font>

# Symptoms

I bought the Gigabyte card purely for the quiet fans, but I’ve found that it cannot and will not run Battlefield 3 without heavy tweaking. Without the tweaks BF3 will, without fail, inside 3 (three) minutes:

* (Silently) Crash to the desktop
* Crash with a BF3 stopped working error
* Crash with a Windows 7 driver failure (like this) <img style="background-image: none; border-bottom: 0px; border-left: 0px; margin: 10px 0px; padding-left: 0px; padding-right: 0px; display: inline; border-top: 0px; border-right: 0px; padding-top: 0px" title="bf3_crash" border="0" alt="bf3_crash" src="https://defragdev.com/blog/images/2011/12/bf3_crash_thumb.png" width="244" height="108" /> 
    
I initially raged against BF3 and called DICE all of the names under the sun as BF games have a history of being horrendously buggy on release (I still crash on loading up for the first time quite a lot so...), but this time around the amount of ranting on forums with BF3 _and_ other DX11 games points to faulty hardware.

# ‘Fixing’ The Problem

Gigabyte users only. Either RMA the card and ask for a different model or...

## Flash the BIOS

Firstly, download [Gigabyte’s EasyBoost utility](http://www.gigabyte.com/support-downloads/utility.aspx?cg=3). Use this tool to flash your Gigabyte 560 Ti OC card to the latest BIOS. It has an auto select feature, so it shouldn’t be too dangerous. **Note**: The only visible effect of this is that the voltage will be upped from 1.000V to 1.037V (verifed using [MSI Afterburner](http://event.msi.com/vga/afterburner/download.htm)).

Try that for size. It _might_ be all you need. Play for a while and see if it’s solid. Some players have had success with just this one step. Unfortunately, I still crashed (albeit a slightly less frequently). With that BIOS ‘fix’, I could play for about 10 minutes before crashing, so it was a step in the right direction.

## Underclock your card to reference 560 Ti levels

Next, download [MSI Afterburner](http://event.msi.com/vga/afterburner/download.htm). It’s made by MSI, but supports most card makes including Gigabyte 560 Ti OCs. Now, use the overclocking functionality to underclock (yes, underclock) your card to the following reference 560 Ti clocks:

* Core Clock (Mhz) : 822
* Shader Clock (Mhz) : 1644
* Memory Clock (Mhz) : 2000

I also underclocked my memory Clock to 1975 just to be sure. Mine looks like this now:

[<img style="background-image: none; border-bottom: 0px; border-left: 0px; margin: 0px; padding-left: 0px; padding-right: 0px; display: inline; border-top: 0px; border-right: 0px; padding-top: 0px" title="image" border="0" alt="image" src="https://defragdev.com/blog/images/2011/12/image_thumb.png" width="205" height="244" />](https://defragdev.com/blog/images/2011/12/image.png)

The difference between these reference(ish) clocks and the factory OC clocks amounts to something like a 2-3% performance difference. BF3 is heavily GPU bound, so instead of getting 40 fps, you’ll probably get ~38 to 39 fps. Not a big deal. It runs beautiful on high settings @ 1920 x 1200 for me using these settings, and I’m a FPS nutter.

It’s obviously shite that you should have to mess around with BIOS flashing and underclock something that fails to run at advertised speeds, but with these changes I can run BF3 for hours on end without crashing. Compared to my record of 3 minutes of gameplay at the beginning of the week, I’ll take that result.

I hope this helps others encountering the same problem.