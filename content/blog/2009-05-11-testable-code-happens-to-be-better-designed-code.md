---
id: 274
title: Benefits of designing for testability
date: 2009-05-11T01:40:23+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=274
#permalink: /?p=274
tags:
  - patterns
  - testing
---
When I started my job as a Software Test Engineer, I had very little knowledge about unit testing. I had a good degree award and a load of acronyms to put on my (in retrospect, rather horrible) CV. I thought I knew a bit about design, encapsulation, patterns, object-oriented programming and all the rest. With a little trepidation, I felt I was ready to face the world as a programmer.

I applied for a few programming jobs at Realtime Worlds and did not succeed. After the first rejection, I did not become disheartened. I did what any sensible young chap would do - I went back to the drawing board. I continually improved my skill, learned c#, created some new programs and re-wrote old programs with the knowledge I'd gleaned. Every so often I'd check the website or speak to my friends who worked there, asking if anything suitable was potentially coming up. Eventually, I landed at Realtime Worlds as a Software Test Engineer.

In an ideal world, I would've succeeded first time. After all, it was my goal to be a software engineer.

### Picture the scene

My tremendously awesome CV plopped onto the doormat, awaiting the arrival of the hiring manager. At 9am on the dot, that fine fellow picked it up and was instantly startled. "Oh my!", he cried, "Who is this remarkable young gentleman programmer who wishes to join our fine establishment?"

The hiring manager sprinted up the stairs, burst into a CV triage meeting - cheeks purple and lungs wheezing - before hurling my golden-tinted paper across the room.  "Look! Look! We've found _him_", he honked. The lead programmers threw their hats in the air, linked arms and then danced a merry dance.

The search was over, and the party went on long into the night (though the party did involve programming a Spectrum emulator for the 3DO).

It would've been great. Well, in many ways yes. In other ways, no. Hindsight being 20/20, I am actually grateful that I didn't get my first job doing normal development. Why?

### Things wot I knew

Firstly, bear in mind the fact that I said I _thought_ I knew about design, encapsulation, this that and the other. I did know a little bit, but I knew precisely **nothing** in the grand scheme of things. Here's the lowdown:

- My knowledge of patterns was the singleton and some others. I did know some others, but it may as well have just been "singleton". Lalala, I can't hear you. I remember the shock when my friend linked my to the <a href="http://steve.yegge.googlepages.com/singleton-considered-stupid">"Singleton considered stupid"</a> article prior to getting a job. "But they're my best mates!", I gasped. "Yeah, but they're stupid", he replied, before jabbing me in the eye with a stick and berating me for my incompetence.

- My idea of simplifying problems by breaking them into smaller systems usually involved multiple managers all interacting via singletons.

- My idea of extensible software was using horribly complicated, deep inheritance hierarchies everywhere. Yeah let's make this base class and then...

- Pretty much everything I wrote was tightly coupled. I thought that I had abstracted things away, but in general I just moved problems around. Nearly every class relied on multiple custom, concrete types. I never used factories.

- I relied on implementation details. I often reached into classes several levels deep. House->GetKitchen()->GetSink()->GetTap(); I didn't just break the <a href="http://en.wikipedia.org/wiki/Law_of_Demeter">Law of Demeter</a>, I dropped it on the ground and used its smashed remains as a (crap) bouncy castle.

I could go on. In short, as a dumb graduate, I was interested in my craft and enjoyed programming, but I had some bad habits and didn't understand why a lot of the things I was doing were flat-out wrong, unmaintanable and are diametrically opposed to the principle of least surprise. However, sometimes you don't find out about these things until you're forced to broach a particular topic.

The reason I'm so glad to be a software test engineer is that all, and I mean **all**, of these coding horrors were laid bare when I started learning how to test properly. When your code is fundamentally untestable, there is no denying it.

### Sowing the seeds

As a newbie, I was tasked with writing tests for a lot of our existing codebase. This meant I was exposed to a lot of different structures and idioms of production code written by **everyone.** Some of it was very easy to test; other parts not so much.

We're a games company and unit testing is not something that has gained widespread acceptance in games. Back then, it was no surprise that the results were variable. I spent months writing loads of tests and it took me _a long time_ to feel like I was doing it in a way that I was happy with.

Anyway, rewind back to when I sucked more than I suck now. Even though I had no idea about what testability concerns should be, I quickly learned through doing. I read articles and kept attempting to write better tests.

- After a couple of weeks, I started rocking back and forth if I saw a static class. "Oh God", I'd cry, "What do I need to initialise then tear down <em>this time</em>?"

- After a month, I hated the sight of any class containing scores of methods, lengthy method bodies, multiple indentations of control flow logic etc. "Jeez, what do I need to do to hit <em>this</em> side of the double nested if statement that's part of a switch which is called in a chain of 8 private methods? If only the logic were split up into nicer chunks..."

- After another month, I started to wonder why many of the tests I was writing were so slow, given that I was only interested in testing one class at a time. "Oh man!", I'd exclaim. "Why do I have to create all these slow thing? Bah, I can't even get at the logic I want to test! If only I could instantiate only what I need and totally control the test environment..."

- After another month, I reasoned that if an interface were to be provided and the dependencies could be abstracted away into 'seams', it made the code infinitely more testable. "Hmm, I see why loose coupling is good..."

- After another month, I wondered why some of the tests were so fragile. When some system or other changed, the tests for an unrelated class would fail! "Oh... that's why singletons are frowned upon. The dependencies are hidden!"

- After another month, a workmate found Misko Hevery's [guide to testability](http://misko.hevery.com/code-reviewers-guide/) and the penny dropped. Like Google's testing blog logo - it was like switching on a light bulb!

Beyond that day, I've kept learning more and more techniques to use as part of my development and testing arsenal. Making my code more testable was the goal, but it has given me so much more. Testability is a great thing, but as with all software engineering techniques, it is not a silver bullet.

The most important thing is that, with seemingly no concerted (separate) effort on my own part, the code I write to be testable is magically a lot better than the way I used to write it.

### Inadvertent Benefits

As Luke Halliwell [succinctly pointed out](http://lukehalliwell.wordpress.com/2009/01/22/a-rule-of-thumb-and-a-silver-bullet/) a while back, testability concerns and good design practices tend to converge. If your code is testable, there's a greater chance that the problem has been broken down into units of work. Read his summary; it definitely coincides with my own experiences thus far.

Actively seeking out solutions to make code more testable as resulted in some extremely valuable lessons - it has exposed me to new techniques (such as [Dependency Injection](http://en.wikipedia.org/wiki/Dependency_injection)) and ways of thinking. These didn't just alter the way I tested, they fundamentally altered the way I approach the writing of software. In the ~x or so years I've been programming, designing for testability has been my single most valuable expedition!

Am I suddenly the world's greatest programmer? Far from it. I know scores of folk at work who can program circles around me. On the other hand, is my code easier to understand, more maintainable, more cohesive and less tightly coupled compared to what I was writing a year or so ago? Undoubtedly. Are there fewer surprises? You bet. Would anyone who had to maintain my code be inclined to hunt me down and murder me? No. They may perform some sort of grievous wounding, but I will live.

I can't believe how much I sucked. I definitely [suck less](http://www.codinghorror.com/blog/archives/000530.html) this year, though.