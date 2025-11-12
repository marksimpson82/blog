+++
title = "MS Wheel Mouse Optical Redux (August 2018)"
tags = ["driver", "games", "hardware", "mouse", "sweetlow", "tips", "windows", "wmo"]
+++
Back on the WMO train again. I was using Sweetlow's signed driver, but it stopped working again, probably due to 
Windows updates. You can find the old guide
[here](@/blog/2017-05-12-ms-wheel-mouse-optical-redux-wmo-1-1-windows-10-x64.md).

I'm on Windows 10 Home 64-bit, version 1803. Here's how to get it working at the time of writing.

The main google result is not the actual official Sweetlow post. It links to a thread on the overclock.net forums that was not made by Sweetlow. Instead, follow the instructions on Sweetlow's official (and up to date!) [post](https://www.overclock.net/forum/375-mice/1589644-usb-mouse-hard-overclocking-2000-hz.html).

Unfortunately, the ‘vanilla' signed driver no longer works for me, but I would recommend trying the main instructions first.

> I had to use a workaround that is covered in his post. Specifically, the part where he says:  
> 2. If you have EHCI (USB2.0) Controller only on version x64 1703+ or any controller on version 1803+ use these drivers and (Test Mode or atsiv method with non Test Mode)

I haven't had any luck with the atsiv method, but the test mode suggestion worked (after a bit of fumbling around).

Here are explicit steps on how to do this workaround. As ever, I will caveat this by saying it may not work for you.

**Backup your files**

  * Backup the following files: 
      * %systemroot%\system32\drivers\usbport.sys
      * %systemroot%\system32\drivers\usbxhci.sys

**Enable test mode to allow unsigned drivers**

  * Open a cmd prompt with admin privileges and type the following commands 
      * `bcdedit -set loadoptions DISABLE_INTEGRITY_CHECKS`
      * `bcdedit -set TESTSIGNING ON`
      * Reboot

**Finally, install the driver**

We're going to download the official Sweetlow package (which contains the installer and versions of the driver) and replace the official driver with a patched version. We will then use the official installer to install a patched driver.

1. Download & unzip <a href="https://www.overclock.net/attachments/45829" rel="nofollow">https://www.overclock.net/attachments/45829</a> (you need an overclock.net account to do this) to a directory called "official"
1. Download & unzip <a href="https://github.com/LordOfMice/hidusbf/blob/master/hidusbfn.zip" rel="nofollow">https://github.com/LordOfMice/hidusbf/blob/master/hidusbfn.zip</a> to a temp directory called "patch"
1. Navigate to "patch"
1. Copy the DRIVER\AMD64\1khz\hidusbf.sys file
1. Navigate to "official"
1. Replace its DRIVER\AMD64\hidusbf.sys + DRIVER\AMD64\1khz\hidusbf.sys with it (I suspect the installer uses the first of these, but I haven't checked for sure, so replace both)
1. Still in "official", run setup.exe
1. Check the "Filter On Device" box
1. Change the rate to 1000hz
1. Click the "Install Service" button
1. Click the "Restart" button
1. Close setup.exe
1. Open mouserate.exe (or browse to <a href="https://zowie.benq.com/en-eu/support/mouse-rate-checker.html" rel="nofollow">https://zowie.benq.com/en-eu/support/mouse-rate-checker.html</a>) and check your hz

If that didn't work, reboot. If you mess it up and your mouse stops working, simply go to device manager, uninstall the WMO via remove device, then unplug it before plugging it back in. You're then OK to try again.