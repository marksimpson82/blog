---
id: 122
title: "Modding: Avoid making the same mistakes that I did #7"
date: 2009-04-04T17:02:24+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=122
#permalink: /?p=122
tags:
  - modding
---
### Forget fancy websites, PR and advertising

When creating Fortress Forever, we generally depended on TFC players who had modding skills to get us up and running. As a result, the moment other TF mods started threatening to spring up, we felt it was a good time to put up a website to ensure that we were visible to anyone interested in working on a Source TF mod. Since we had a website set up, we added all of the usual _content_ to it, got some forums and started doing interviews and media releases etc.

In hindsight, I feel that running the website, maintaining forums and dealing with the community & modding sites at such an early stage was a big error. The feedback on the forums did give us some genuinely good ideas, but in general it was much more hassle than it was worth. Let's think rationally about this for a second: We were talking to people about something we had not yet built. People were offering feedback on things that they had not yet played. For every salient point, there was probably 100 useless posts containing noise, tattle and flames (i.e. just a normal forum). This goes back to my previous post about design: You can talk it to death. It's much more useful to actually do it and then iterate. If you spend hours a week promising the moon on a stick or justifying choices you have yet to implement, you could spend those hours doing something tangible.

After a year or so, FF's forums had thousands of users. Trolls, elitists and cliques build up over the years, especially if people are discussing .. nothing (or how long it has been between media releases etc.) There were even a few hack attempts. The point is that all of this stuff takes time to set up and maintain. It didn't help us get much closer to our goal of shipping the mod.

I should also mention that the FF forums also had thousands of normal, nice and helpful users :)

### Another good reason for maintaining a low profile

If your mod goes public and you make a big song and dance about it, it makes you a much more appealing target for pissed off ex-members of the mod or hackers in general. If it's a small project and nobody has heard of it, there's limited value in releasing source code or bitching to the masses about the mod. However, it's viewed as a 'big' mod with high coverage on community sites, you're a much more satisfying target for a disgruntled modder.

As far as I know we weren't ever targeted by an ex-member, but I wouldn't have been surprised if someone had thought about it. There's always the risk of fallings out and friction between folk, that's life. Some people take it particularly badly and will try to get back at you by trying to trash the mod in any way possible.

We did however get 'hacked' at some point. The 'hacker' acquired a build of the mod from our SVN repository, but it was a beta version that had reams of the server code removed (so it would just crash if you tried to run a server). As a result it could only connect to our official beta servers, which were themselves protected via SteamID checks. The 'hacker' threatened to reverse engineer and leak the build, but ultimately failed because our precautions were good enough. If we had quietly gone about our business, I doubt the person would've gone to such lengths to try and fuck with us. I believe that Black Mesa suffered the ignominy of having their hard work leaked a few years back, so it is definitely something to be aware of.

### If you insist...

If you are in a situation where you definitely do need a website of some sort (typically to attract modders to work on your project), just keep it simple. Post an outline of what your mod is all about, a description of the modders working on it, the skills you are interested in and also some images of the work done so far (if available).

If people show an interest in what you're doing, then you can always periodically show off some cool stuff, just try not to make a big deal out of such things until you're actually approaching some sort of release. Again, for every mod that makes it, there's probably 20 that fold without shipping anything. If you have something to release, start to think about advertising it. Until then, forget it!