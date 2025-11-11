---
id: 570
title: Data oriented design links
date: 2010-07-21T18:22:11+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=570
#permalink: /?p=570
tags:
  - games
  - patterns
---
I've been doing a little reading around data oriented design of late and thought it was worth sharing some interesting links. Here's my distillation of the reading I've done so far (caveat: I may be talking balls).

**Prelude: Battling Dogma**

All too often, games programmers butt up against dogmatic catch-all declarations of "virtual functions are slow!" For the general case, [this can be proved as a nonsense](http://assemblyrequired.crashworks.org/2009/01/19/how-slow-are-virtual-functions-really/) as virtual function calls are blatantly not slow! They're very, very fast. However, if someone said instead, "virtual functions are slow when iterating over large collections of heterogeneous types because of cache misses" then that's another matter, entirely. Unfortunately, we all too often hear the former declaration rather than the latter. It's neither compelling (as we can prove it is incorrect in the general case) nor edifying. Most programmers like to learn things, so it's nice to read some illuminating articles about a touchy subject.

**The gist of it**

Data oriented design is based on examining the access patterns and transformations performed on data. The code is then structured to make it data-centric by using a combination of changes to the type of data stored, the way it's laid out in memory and the ordering of the data, amongst other things. An instructive example of this is given in the BitSquid article where animation data is ordered by time, as this best fits the common access pattern that a game would use. Another particularly useful example is where data structures are broken up into multiple parts so that more of the data used by common operations fits into the cache.

The main benefit is reducing cache misses, but a nice side effect is the increased opportunities for parallelisation. A lot of this stuff is well-known and as old as the hills, but in my experience it's often been bundled with dubious practices, so it's nice to see some practical, tangible examples of when and why you should apply such techniques.

**Links**

- [Games from Within Article](http://gamesfromwithin.com/data-oriented-design) - A high level article; Noel works through some disadvantages of object oriented design and then cites some examples where data oriented design can be employed to speed things up.

- [Pitfalls of Object Oriented Programming](http://research.scee.net/files/presentations/gcapaustralia09/Pitfalls_of_Object_Oriented_Programming_GCAP_09.pdf) - Tony Albrecht of Sony has some very interesting diagrams, slides, timings and statistics that lay out the costs of cache misses and branch prediction failures with very specific examples, then optimises via various means.

- [Practical Examples in Data Oriented Design](http://bitsquid.blogspot.com/2010/05/practical-examples-in-data-oriented.html) - Bitsquid engine programmers dish out some examples of designing with data access in mind. Higher level that the Sony presentation, but also very useful.

- [GameDev discussion thread](http://www.gamedev.net/community/forums/topic.asp?topic_id=575076) - Generally useful discussion thread. Has some code examples, too.

- [Typical C++ Bullshit](http://macton.smugmug.com/gallery/8936708_T6zQX/1/593426709_ZX4pZ#593426709_ZX4pZ) - Code annotated by cranky post-it notes. Not exactly an illuminating discussion or an article as such, but worth including for completeness.

**Related**

- [Game Entity Systems](http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/) ****- The T=Machine blog has a series of posts on designing game entity systems. One part of the series deals with processing homogeneous data and why this makes it fast / more easily parallelisable.