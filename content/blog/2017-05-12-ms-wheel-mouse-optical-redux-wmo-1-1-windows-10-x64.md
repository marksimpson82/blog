+++
title = "MS Wheel Mouse Optical Redux (WMO 1.1 & Windows 10 x64)"
tags = ["gaming", "hardware", "mouse", "overclocking", "tips", "wmo"]
+++
Back in 2011, I wrote a 
[fairly gushing post](@/blog/2011-07-15-ms-wheel-mouse-optical-wmo-1-1.md) about the Microsoft WMO 1.1/1.1a. 
It’s a great mouse. It really is.

<img style="margin: 10px 0px;" src="https://defragdev.com/blog/images/2011/07/image1.png" width="240" height="240" /> 

## The end of my WMO

Sadly, in late 2016, the venerable WMO gave up the ghost – its death certificate listed a faulty cable. Basically, I’d be playing Overwatch and it’d randomly disconnect, then reconnect. I’m not a technician, so I binned it.

I then bought a Steelseries Rival 100, as I needed a stopgap mouse. The Rival 100 is a decent mouse, but its shape doesn’t agree with me (it’s too narrow), and it’s a touch too heavy for my tastes.

## Finding a replacement mouse model

I decided to try and track down a decent WMO replacement. After a bit of a hunt, I couldn’t find anything that’s 100% suitable; some people recommend Zowies like the EC2-A or FK1, and others like the Razer DeathAdder Chroma.

It’s tough to track down accurate information regarding the unpackaged weight of the mouse, too. The WMO weighed in at ~80g, and in my opinion is better for it.

Furthermore, I don’t want a mouse with stupid cloud software (S3 is down? Well, not sure how to load your mouse settings man!), and I’m not really a fan of spending £60 on a mouse in what is essentially a blind purchase. I might love it, but I might hate it.

If you can walk into a decently-sized PC store and try out a load of mice, I’d recommend just forgetting about the WMO and finding something new.

## However, if you’re stubborn...

In the end, I decided to buy another WMO. They’ve long since been discontinued, so the main options nowadays are ebay and second-hand sites.

Personally, I bought some refurbished ones, plus a new one that was still in its (rather worn) box – it’d been sat on a shelf for 10 years, ha! I’d recommend going this route – there’s plenty of obscure product numbers & sites listing good/bad sensors, so you can do a bit of googling based on the seller’s pictures. It’s not an exact science, but the mice tend to be so cheap that it doesn’t matter if you buy a dud or two. My total outlay was about £25 for 3 mice. The two I’ve tested have the same product number of X802382. Both work fine.

Finally, [modded WMOs](http://www.ebay.com/itm/Microsoft-Wheel-Mouse-Optical-WMO-Steelseries-MOD-100-NEW-5-Colors-/121179666270?pt=LH_DefaultDomain_0&var=&hash=item61d44f5bbb&rmvSB=true) from a specific seller on ebay are available, and the seller has a good reputation, so he’s perhaps worth a look.

## Overclocking – harder than it used to be

I briefly touched on this in my previous post from 2011: if you don’t overclock the polling rate, the mouse performs worse. Depending on your sensitivity settings, this can be a deal-breaker and render it unusable.

The tl;dr here is that the WMO (and its stablemates) offers “perfect control” to a speed up to 1m/s, but exhibits negative acceleration beyond this speed _[unless you overclock the mouse polling rate](http://www.overclock.net/t/1597441/digitally-signed-sweetlow-1000hz-mouse-driver)_. I won’t warble on about the nuts and bolts of this too much, as there’s a great [esreality article](http://www.esreality.com/?a=longpost&id=1265679&page=4) about it that explains it better than I can.

What I will say is that, if you’re a high sensitivity gamer and don’t fling the mouse around a lot, this may not be a significant issue. However, I play Overwatch with an eDPI of 3.1k (450 CPI * 7 sensitivity) which equates to roughly 43 cm for a 360. This is on the lower sensitivity side of things for OW. Hitting a 180 means travelling ~20cm across the pad. Unfortunately, I _easily_ hit the negative acceleration threshold @ 125hz, and my 180 degree turn looks more like a 100 degree bout of confusion.

I’d had overclocking working with Windows 10 x64 previously using an unsigned driver in test mode, but for whatever reason, I just couldn’t get it to hit better than 125hz using [Sweetlow’s new signed driver](http://www.overclock.net/t/1597441/digitally-signed-sweetlow-1000hz-mouse-driver). It would downclock OK (so I could run it at 30hz), so I just assumed I’d got a dud mouse since it wouldn’t go past the default settings. This was not the case.

## The state of play with the community-created driver

The guy that wrote the driver has showed a lot of ingenuity, and the community came together to raise the funds to sign the driver. The downside is that since it’s niche bit of kit, so getting help relies on a handful of folk. The readme is a little confusing and you have to download the files from a forum’s attachments and/or work your way through multiple broken links (sorry, not going to take point here as these files change frequently).

There’s also a huge thread full of “HLAP! It won’t work!” posts, and I don’t think there’s an FAQ, so you have to sift through 50+ page threads full of information that is usually not terribly relevant to your particular issue. I had almost given up when I managed to get it working!

So here’s the current state of affairs (May 2017):

* A signed driver exists which means you shouldn’t need to install an unsigned driver (this is good!)
* Its certificate (which must be renewed yearly, I believe) expired or is about to expire (this is bad!)
* A recent Windows 10 Content Creators update broke the signed driver on Windows 10 x64 (this is also bad!)
* It will _probably_ work for you _unless_ you’re on Windows 10 x64 with the latest updates.
* Various USB issues exist (haven’t personally run into this, but there’s lots of chat about disabling secure boot, xHCI and various other bits of hand-waving going on).
* There’s also an alternative overclock which involves USB 3.0, but I’ve not touched that one.

Sweetlow is doing a great job considering it’s just a side hobby for him, and he’s helping a lot of people. I thought I could help by detailing my problem & solution here.

## May 2017, Windows 10 x64

I will preface this by saying it’s not a great solution. An unsigned driver is involved, just like olden times. Sweetlow has said he’ll roll these fixes into the new signed driver. In the meantime, here’s how I got it working.

Note that this involves running windows with some system settings changed. Unless you’re comfortable with this, don’t do it.

I’ve also heard rumblings about some games viewing this as dodgy (from an anti-cheat perspective), but haven’t confirmed it. I ran all games for years with exactly the same method without issue.

* Backup the following files:
  * %systemroot%\system32\drivers\usbport.sys  
  * %systemroot%\system32\drivers\usbxhci.sys
* Create an account on overclock.net
* Download the [signed driver](http://www.overclock.net/t/1597441/digitally-signed-sweetlow-1000hz-mouse-driver) and unzip it somewhere
* Download the updated (non-signed) hidusbf.sys file from [this post](http://www.overclock.net/t/1597441/digitally-signed-sweetlow-1000hz-mouse-driver/480#post_25977633)
* Replace the hidusbf.sys in the signed driver directory (DRIVER/AMD64/hidusbf.sys) with the one you just grabbed
* Open a cmd prompt with admin privileges and type the following commands 
  * `bcdedit -set loadoptions DISABLE_INTEGRITY_CHECKS`
  * `bcdedit -set TESTSIGNING ON`
* Reboot
* Browse to the signed driver directory
* Right click HIDUSBF.INF and choose “install”
* Run Setup.exe
* Check the “filter” box
* Set the polling rate to 1000hz or whatever you want
* Click “install service”
* Click “restart” (the button in the setup.exe, not restart your PC!)
* [Check your mouserate](http://zowie.benq.com/en/support/mouse-rate-checker.html) – it should be north of 125hz

Thanks to sweetlow and co for this bit of magic.

## Result: 1000hz

My WMO is running at 1000hz again, and the perfect control speed is noticeably improved; it is now ~1.5m/s, which is more difficult to hit at my sensitivity, but certainly possible. If I really whip the mouse into a 180, the uneven turning is still evident, though much less pronounced. I’ll see how badly this affects my game and either persevere, or get a new mouse.

The WMO has its flaws and isn’t appropriate for everyone. If you play with a similar or even lower sensitivity than me, I would recommend looking into a more modern mouse, as the WMO won’t keep up. [Ryujehong’s 70+cm/360](https://www.youtube.com/watch?v=74X-irNEK1M) would certainly not agree with the WMO!

## Addendum: Stripping the mouse cable

The WMO mouse cable really sucks. It’s extremely stiff and doesn’t straighten out easily; this results in snagging and uneven resistance as you move the mouse around, causing the cable to bend and coil. To remedy this, you can strip the outer cable sheath – just (carefully) run a sharp knife around the circumference of the cable, then strip the sheath by gently tugging on it. There is a copper inner sheath, so it should be fine.

You don’t need to strip the entire cable, just a section of it close to the mouse body. I made a cut about an inch from the mouse body, then another half a metre up the cable. I then tugged at the sheath and removed the section. Result: the mouse cable is much more pliable. Can’t really say whether this will affect its durability, but I did this on a £6 second-hander, so I don’t really care too much.

## Post-amble: I bought a Logitech G403 and love it

I played with the WMO for a week or so; the negative acceleration coupled with my low sensitivity renders it unsuitable. I decided to try something new.

So what to do?. [Rocketjumpninja's website](http://www.rocketjumpninja.com/top-40/) has some great mouse review articles & youtube links, including detailed size comparisons / side-by-side videos of various popular mice.

Given that my hands are fairly long (22cm or so) and I palm grip when gaming, I thought the Zowie EC1-A or the Razer DeathAdder would be good. However,&nbsp;I tried the Zowie EC1-A and it didn't suit me. It was a good match for me length-wise and was comfortable to rest my hand on, but it's too wide for me to pick up without changing the way I grip it.

If you have massive hams for hands, definitely check out the EC1-A. The sensor is great, and it has a few other wonderful features, namely a DPI switch being on the base of the mouse ("let's change DPI to go into sniper mode!" said nobody ever, apart from marketing guys) and zero setup / drivers. True plug 'n' play.

After sending it back, I noticed RJN's videos featured a Logitech G403. The G403 is much larger than the Steelseries Rival 100, and somewhere between the sizes of the EC1-A and the EC2-A. Given that I wanted a larger mouse, but not as big as the EC1-A, the Logitech G403 fitted the bill. It is perfect for my hand size.

Positives:

  * I like the shape even better than the WMO / EC1-A.
  * It's light. Not quite as light as the WMO, but within 10g. The extra 10g is not noticeable as...
  * ... it glides much better and faster than any other mouse I've tried
  * The cable slides over a cloth pad easily and doesn't twist or snag.
  * The sensor is amazing.
  * The DPI switch cycles between 400 / 800 / 1600 / 3200 DPI without requiring drivers.
  * You don't need to install any software whatsoever unless you want to customise it (I don't).

Negatives:

  * It's £60, for crying out loud! I managed to get it on sale for £40, but the normal retail price is very steep.
  * The cable is very thick. While its weight is not an issue, it doesn't fit in most mouse bungees (razer bungee says: nope).
  * The DPI switch is on top of the mouse. It's hard to press accidentally, but it's still there. Zowie wins this round.
  * Logitech's customisation software is a 100+ MB installer. Balls to that! (This is also a major reason I won't buy razer mice.)

I'm pretty sure that my mouse-buying days are over for another 5 years. What I take from this spate of experimentation is that there is no 'amazing' mouse that beats all others. It all depends on your hand size, shape and grip style. Try out some mice and see what suits you rather than buying the "best" mouse with the most positive reviews.