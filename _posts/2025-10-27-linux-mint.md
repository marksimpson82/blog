---
title: "Windows 10 support ending? Linux Mint for my parents"
date: 2025-10-27T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - linux
  - windows
  - tpm
---

As a long-in-the-tooth software engineer, I'm getting to the end of my tether with Windows. I've lived through (and used) practically every version of Windows from 3.1 through to Windows 11, and the direction of travel is negative. Into the sewer, even.

I've used numerous versions as concerned citizen, student, adult and alleged professional:
- Windows 3.1
- Windows 95
- Windows 98
- Windows 2k
- Windows ME (lol)
- Windows XP
- Windows Vista
- Windows 7 (I didn't even bother with 8)
- Windows 10
- Windows 11

There were a few high points in there. Windows 7 is up there, as is 98 and 2k (which I used because the mouse acceleration promised to make me a God tier FPS player -- it did not). Hell, even the last years of Vista seemed vaguely pleasant. After the relative simplicity of Windows 7 it's been downhill all the way, though.

## The Slow Death of Windows 10 
My memory of the first revision of Windows 10 is unreliable. What I can say for sure is that each new revision of Windows 10 came crammed full of bloat, advertising, spyware and even bullshit like pre-installed LinkedIn apps. I've got a PowerShell script (plus some manual instructions) to run after installing Windows, and each time I have to install Windows, the list needs updated.

Here's a summary:

How do I...
- Avoid creating a Microsoft account when installing the OS?
- Remove adverts from my lock screen?
- Remove celebrity news from my taskbar?
- Delete all of the bundled bullshit apps and bloatware?
- Uninstall all the XBox shit?
- Disable Cortana?
- Remove Bing search integration from the start menu?
- Lock down all of the privacy settings?

This is hostile to the nth degree and completely direspects the user.

## Windows 11 - Even Worse
I 'upgraded' to Windows 11 a few years back and it was just as bad, if not worse. There were a few more usability issues around context menus and UI consistency (how many flavours of menus are there now? When doing any kind of involved configuration, you have to drop back to Windows 95 era menus anyway!)

I binned it and went back to Windows 10.

## Why Stay on Windows, and can we use Linux?
I use MacOS at work and the only thing keeping me on Windows on my desktop is gaming. However, Linux is becoming more and more of a realistic player when it comes to gaming. I play FPS games that often have kernel anti-cheat (which don't tend to work with non-Windows OSes), so there's still a bit of a gap.

However, my parents have been running Windows since the 7 days, and guess what, they just tend to use their PC for web browsing and not much else. Could I chuck Linux on it and save them the Windows 11 experience? Also, many users will be running old hardware with no [Trusted Platform Module (TPM)](https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/trusted-platform-module-overview). 

If you don't have a motherboard with TPM, you cannot install Windows 11 (if you're unsure, go check your BIOS -- my 2017 motherboard had one, but it was disabled by default). Anyway, if you just want to browse the web, old hardware shouldn't be thrown away to satisfy the spyware gods! If the hardware is capable, let's use Linux!

## Fedora in the Year 2018
I've had a few aborted attempts at the Linux Desktop. The last one was ~2018 using Fedora for AI work stuff, and it was still a pain in the arse. My install ended with a bricked machine.

I installed the OS and spent ages dicking about getting the NVIDIA GPU drivers installed correctly. I then customised the OS and programs to my liking. A few hours later, I didn't pin my NVIDIA driver package and bricked the machine doing `dnf upgrade` and wasted the best part of a day. Oops. Anyway, my point is it was rough around the edges.

## Linux Mint in the Year 2025
This time around, I plumped for [Linux Mint](https://linuxmint.com/). I followed the instructions, created a bootable USB pen drive and got stuck in. 15 minutes later I had a working Linux install with fully updated NVIDIA drivers, rolling backups and all of the basics working. Firefox was ready to go with uBlock Origin and audio worked perfectly. I didn't notice any jank, advertising or spyware being slyly included, either (fancy that).

All in all, a very smooth experience. If you have friends or relatives that are in the same situation, it's well worth a go. I can't guarantee that your games will work with steam or [Wine](https://www.winehq.org/), but if you're just browsing it'll do the trick.

Might be worth trying a dual boot soon on my home desktop, too.
