---
id: 631
title: MS Wheel Mouse Optical (WMO 1.1)
date: 2011-07-15T04:54:59+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=631
#permalink: /?p=631
tags:
  - angle snapping
  - desk
  - games
  - gaming
  - misc
  - mouse
  - mouse pad
  - sensitivity
  - tips
  - wmo
---
## I’m an addict

As a first person shooter (FPS) addict, I play a <span style="text-decoration: line-through;">fair amount</span> shitload of games. I racked up a god-awful number of hours in Team Fortress Classic (I would conservatively estimate over 3000, on account of the fact I played it on and off for several years), 1400+ of Battlefield 2 and now 1000+ of Left 4 Dead. I average ~1 hour a day. I like to tell myself it’s a small time sink and I’m not wasting my life.

In that time I’ve gone through countless mice, mouse pads and a few desks, too. If you <span style="text-decoration: line-through;">waste</span> spend an inordinately large amount of time doing something, it’s worth making sure that your time-wasting is enjoyable as possible. I recently bought a new mouse. Here is some _highly interesting*_ discourse for mouse enthusiasts.

This post covers choosing a mouse, setting it up and then rejoicing in shooting pixels more accurately.

Everyone else: **I am warning you. Look away now**.

_*may not be true_

## Caveat Emptor

I’ve been gleefully using MX5xx series mice for the best part of a decade. The MX518 is a fine, spangly beast. It looks a bit like this:

**An MX518, yesterday.**

[<img style="background-image: none; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border: 0px;" title="image" src="https://defragdev.com/blog/images/2011/07/image_thumb.png" alt="image" width="224" height="224" border="0" />](https://defragdev.com/blog/images/2011/07/image.png)

However, I recently stumbled across the ‘feature’ the MX518 has that’s commonly referred to as “angle snapping”, “prediction” or “correction”. What is angle snapping? Well, at the hardware or driver level, if your movements stay under some arbitrary threshold, the mouse input is subtly altered to keep your ‘lines’ straight.

Here’s the effect in action. A common test is to draw some horizontal and vertical lines in MS Paint. Notice that my MX518-created lines are eerily straight for large sections. If you’re pixel aiming at someone’s head with a rifle, this is not helpful.

[<img style="background-image: none; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border: 0px;" title="mouse_lines" src="https://defragdev.com/blog/images/2011/07/mouse_lines_thumb.png" alt="mouse_lines" width="244" height="244" border="0" />](https://defragdev.com/blog/images/2011/07/mouse_lines.png)

**Note:** This is a feature that is found in several mice, including gaming mice. In some cases (such as the Logitech G series and the Razer Death Adder), you can disable the “feature” using the driver. As that bloke off Art Attack used to say, “Try it yourself.”

## Time for a Change

The MX518 I use at work (I have two) recently had a wheely bad fault and, having discovered the most-likely-non-issue that is angle snapping, I decided to unnecessarily obsess over it and buy something else.

Because that will make me a Quake Live Pro, of course... (oh and sometimes it’s fun to change things)

<img class="wlEmoticon wlEmoticon-smile" style="border-style: none;" src="https://defragdev.com/blog/images/2011/07/wlEmoticon-smile.png" alt="Smile" /> 

## Things to be aware of

Before I delve into specifics, here’s some guidelines for purchasing a new gaming mouse.

### Laser Mice Suck

Firstly, steer well clear of Laser Mice - their tracking sucks. They're expensive. Even people who are endorsed by these brands [don’t use these mice](http://news.fatal1ty.com/fatal1ty-blog/fatal1ty-frags-blog-3rd-frag-mouse-sensitivity/) – laser has not yet caught up with the best optical has to offer, so don’t be fooled by the notion that newer is better.

### DPI is overrated

All of this DPI nonsense seems to have little to do with mouse performance and tracking characteristics. All a higher DPI count seems to do is multiply your sensitivity by a factor using hardware and/or a mouse driver (much the same as turning up your sensitivity in windows and/or ingame).

Older mice with lower DPI can potentially track better than newer laser mice with 5600000000000 bajillion DPI. In short, it’s largely a marketing gimmick.

Most of the professional quake players [use 400 or 800 DPI](http://www.esreality.com/index.php?a=post&id=2009534) coupled with a low sensitivity, so why would you ever need a 5600 DPI mouse? Answers on a postcard.

### Mouse Drivers Aren’t Always Needed

If your mouse is perfectly serviceable without installing drivers, try the mouse both with and without the drivers. I’ve had mice that worked well both with and without. I used the setpoint drivers for my MX518 solely to turn off the silly DPI switching buttons, but I’m not using any drivers with my new mouse.

### Kill Windows Mouse Acceleration

Like [Poison Sockets](http://www.youtube.com/watch?v=D2gqThOfHu4), Windows Mouse Acceleration is a hazard to your health. It’s terrible. [Switch it off](http://www.techpowerup.com/downloads/763/CPL_Mouse_Fix.html) using the [CPL mouse fix](http://www.techpowerup.com/downloads/763/CPL_Mouse_Fix.html). This version works with Windows 7 64 bit – I can’t guarantee anything else, but there’s another version that works with XP floating around.

Mouse acceleration means that physical distance you move the mouse isn’t the sole factor for your aiming. If you use it, it should be a conscious decision, not something foisted upon you by windows in a ham-fisted fashion.

If you insist on using mouse acceleration, either use the driver settings for your mouse or, even better, set up acceleration using in-game settings (newish half life and quake-based engine games offer customisable acceleration settings).

### Negative Acceleration

[Even with today’s space-age technology and fretful nerdery, mouse tracking is not yet perfect.](http://www.esreality.com/index.php?a=longpost&id=1265679&page=4)

Most optical gaming mice on the market today can handle extreme speeds without losing their minds (as in, it’s almost humanly impossible to totally totally baffle the sensor while furiously turning around). However, if you play with a low sensitivity and use a large mouse mat (I’m talking at least > 20cm of mouse movement to turn 360 degrees) there is the possibility of suffering from negative acceleration.

Negative acceleration occurs when the sensor continues to recognise input, but cannot accurately track the distance covered. The faster you move the mouse, the less distance is registered. This manifests itself in fast movements (such as flicking the mouse to turn around) not turning you as much as if you’d performed the movement slowly.

The optimum mouse setting is one where physically moving the mouse the same distance maps to the same logical game input. Negative acceleration erodes this consistency.

[The ESRreality MouseScore](http://www.esreality.com/index.php?a=longpost&id=1265679&page=4) offers the clearest explanation.

It should be noted that, but for all the worst offenders, this is only a concern for low sensitivity gamers, and certain mice have workarounds available ([such as increasing the USB polling rate](http://www.overclock.net/mice/596276-changing-usb-polling-rate-1000hz-lower.html) via Windows).

## The Contenders

After researching the pitfalls, I did a cursory bit of [reading around](http://www.esreality.com/index.php?a=post&id=1836580) and discovered that roughly half of the best competitive Quake Live players use (or used) one of the following (crappy-looking) mice:

<li style="list-style-type: none">
  <ul>
    <li>
      <a href="http://www.microsoft.com/uk/hardware/mouseandkeyboard/productdetails.aspx?pid=008">Microsoft Wheel Mouse Optical</a> (commonly abbreviated to <strong>WMO</strong> or <strong>WMO 1.1</strong>),
    </li>
    <li>
      <a href="http://www.microsoft.com/uk/hardware/oempartners/ProductDetails.aspx?pid=018">IntelliMouse Optical</a> (<strong>IMO</strong>)
    </li>
    <li>
      <a href="http://www.microsoft.com/hardware/en-us/p/intellimouse-explorer-3.0">IntelliMouse Explorer 3.0</a> (<strong>IME 3.0</strong>).
    </li>
  </ul>
</li>

None of these mice is billed as a gaming mouse and they’re all dirt cheap. Bizarrely, Microsoft don’t really talk up this fact or try to cash in. They’re like a trio of unassuming murderers living next door. Strange.

All 3 feature the same optical sensor. The differences are just the shape and the available buttons. The **WMO** is ambidextrous; the **IMO** is the same shape but has some extra side buttons. The **IME 3.0** is also a very similar shape, but is right-handed and has the extra buttons. Gamers tend to favour the **WMO** or the **IME 3.0**.

The negatives of each of these are all similar. Firstly, without altering the USB polling rate, the sensor performs worse than the likes of the Death Adder. Secondly, the wheel has a mind of its own. Slamming the mouse down can force a button press. For this reason, many players unbind the wheel and mouse 3 and rely on keyboard binds.

You can find the **WMO** or **IMO** for £8 to £15 and the **IME 3.0** for £20.

The rest of the mice like the Death Adder all have strong reviews, but furtively slither into the £40+ price bracket. As a Scottish miser, £40+ is a lot of clams for a pointy thing, so I baulked at the prospect.

Anyway, I chose...

## The Wheel Mouse Optical 1.1

After drinking in the details posted in various nerd forums, I plumped for the WMO 1.1 at [£14.99 from Maplins](http://www.maplin.co.uk/microsoft-wheel-mouse-optical-33021) (product code: D66-00074) ordered via Amazon.

As far as I can tell, there’s no problem with stock or versions. If you get one that was manufactured in the last 90 years, it ought to be a version with the sensor that’s good for gaming.

**The WMO 1.1**

[<img style="background-image: none; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border: 0px;" title="image" src="https://defragdev.com/blog/images/2011/07/image_thumb1.png" alt="image" width="244" height="244" border="0" />](https://defragdev.com/blog/images/2011/07/image1.png)

My first port of call was to uninstall my old logitech setpoint mouse drivers. I then plugged in the new mouse and cancelled the intellipoint driver installation process. There’s no need to install drivers for this mouse, so it’s one less thing to worry about.

Next, I installed [the CPL mouse fix](http://www.techpowerup.com/downloads/763/CPL_Mouse_Fix.html) to remove windows mouse acceleration.

Finally, to minimise the chances of encountering negative acceleration, I overclocked my USB polling rate to 500hz. This was quite fiddly to do, but beyond a few reboots and Avira complaining about phantom viruses, it wasn’t a big deal.

Overclocking the USB polling rate increases the ‘perfect control’ region from 1 m/s up to 1.5 m/s, so unless you _really_ throw it around with a miniscule sensitivity, negative acceleration shouldn’t be a concern.

A quick test showed everything was in order.

## Desk and Mousepad

As an avid PC headbanger, I’ve always favoured large desks. In fact, I don’t understand why many PC owners fret over mice and monitors but often overlook the cornerstone of the PC experience: The desk and the chair.

I’m using a [Influx Curva 1200 Right-Handed Wave Desk](http://www.ukofficedirect.co.uk/influx-curva-1200-desk-wave-prd_154850.aspx) coupled with a [Steelseries QcK+](http://shop.steelseries.com/index.php/surfaces/steelseries-qck-plus.html) mouse pad. Both are fantastic products. The Curva is solidly constructed, is a perfect height and affords me plenty of room.

I’ve got a 24” + 20” monitor dual screen setup, and there’s still room for a 45cm mouse mat and a few other bits and pieces. At £150 it’s not a budget buy, but given how much I use my PC, I think it’s well worth it.

[<img style="background-image: none; margin: 0px; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border: 0px;" title="image" src="https://defragdev.com/blog/images/2011/07/image_thumb2.png" alt="image" width="244" height="244" border="0" />](https://defragdev.com/blog/images/2011/07/image2.png) + [<img style="background-image: none; margin: 0px; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border: 0px;" title="image" src="https://defragdev.com/blog/images/2011/07/image_thumb3.png" alt="image" width="244" height="244" border="0" />](https://defragdev.com/blog/images/2011/07/image3.png)

Regarding the size of the mousepad: I used to think anything over 30 cm was overkill, but having a 45 cm pad makes a large difference. It covers such a large part of my desk that I no longer have to worry about positioning the pad – it’s _everywhere_, so I can get comfy. A decade ago, my TFC clanmates used to constantly mock me for [my OCD style mouse mat positioning](http://defrag.urbanup.com/87179). The words still ring in my ears. I cried sometimes, but no longer.

Compared to the standard size QcK, it also affords me the luxury of using a lower mouse sensitivity.

## Sensitivity

I’m an arm player in that I use my forearm to move the mouse as opposed to my wrist/fingers. I used to be a high sensitivity wrist/fingers player when I had a small desk. I prefer using my arm; it’s more precise and I suffer from fewer PC-related mousing strains.

One sweep across the entire pad turns about 400 degrees (so probably about ~40cm for a 360 degree turn). Because of its weight, this was slightly cumbersome with the MX518. The WMO is much lighter and glides easily.

Generally speaking, the lower your mouse sensitivity, the more precise you can be for picking out enemies. A low mouse sensitivity is not a panacea, nor will it make you, me or anyone else a PRO GAMER!1, but I’ve switched around over the years and I keep gravitating towards lower and lower sensitivities.

Also, once you’re familiar with a game, the need to sharply turn around often abates as you react less and predict more.

## Testing and Conclusion

I’m impressed with the WMO. For £14.99 and a bit of tinkering, it’s a great mouse and, with my settings, the tracking seems to be borderline flawless.

It’s definitely not as grippy as the MX5XX series so if you’re a sweaty git, you may find it becomes slippery due to the lack of a rubbery finish. Thankfully, I don’t sweat at all when sitting at the PC so this is not an issue for me.

Also, the shape is perfectly fine; I prefer the shape of the MX5XX but this is better than adequate. Everyone will have their own preferences when it comes to shape.

The tracking is borderline flawless and its lightness means it glides much more easily than other more tubby mice.

The only real downsides I’ve encountered were the phantom clicking mouse wheel issue and having to mess around with USB polling rates. If you can live with these two issues, then I’d strongly recommend trying it out. For £15, you won’t do much better.

Yes, I am a nerd.

## Additional References

[Fragtality’s epic gaming mice guide](http://forums.majorleaguegaming.com/topic/165005-fragtalitys-epic-gaming-mice-guide-for-pc-shooting-games/)