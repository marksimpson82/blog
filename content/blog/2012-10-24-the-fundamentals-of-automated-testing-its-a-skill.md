+++
title = "The fundamentals of unit testing: It's a skill"
tags = ["fundamentals of unit testing", "testing", "tips"]
path = "/blog/2012/10/24/the-fundamentals-of-automated-testing-its-a-skill.html"
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

The first thing I'm writing about is probably the most important. This is a bit of a meandering tale, but it is crucial to understanding the pitfalls of automated testing.

## A Cautionary Tale

Back in the day at Realtime Worlds (the best part of 5 years ago), when it came to automated testing we were trying to pull ourselves up by our bootstraps. Most people (including myself) didn't have much of a clue about automated testing. It was a pretty bold move for a games company to try it on a large scale, but it took a very long time for it to pay any benefits. In fact, given the lackadaisical approach and lack of buy-in, it probably had an overall negative effect in the majority of areas. 

In my first job fresh out of university, I had the nominal title of Junior Test Engineer. At first, it was our job to try and write extra tests that developers missed, debug failing tests and generally take care of the build. I soon learned to be very cynical.

As you can imagine, it wasn't very effective (hint: the larger the distance between a person's actions and the consequences of said actions, the less of an interest they will take). I would characterise it as a baptism of fire. Thanks to spending all day, every day, on automated testing, I acquired a large amount of knowledge by trial and error and learning with my colleagues. That knowledge was eventually ploughed back into the team in a supporting role.

Anyway, when I first joined, it was common to see stuff like this:

```cs
[Test]  
public void TestInverse()  
{  
  var m = Matrix.Identity;  

  Assert.That(m.Inverse(), Is.EqualTo(m));  
}
```

.. or worse, this:

```cs
[Test]  
public void Test1()
{  
  var m1 = Matrix.Identity;  
  Assert.That(m, Is.Not.Null);  
  var m2 = Matrix.Identity;  
  var m3 = Matrix.Multiply(m1, m2);  
  Assert.That(m3, Is.EqualTo(Matrix.Identity));  
  var m4 = m2 + m3;  
  Assert.That(m4, Is.EqualTo(new Matrix( 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0));  
  var m5 = m1 - m2;  
  Assert.That(m5, Is.EqualTo(Matrix.Zero));  
}
```

These tests aren't good. But they were _everywhere_.

This is not intended as a slight to whoever wrote tests like these because _they were all like that._ Developers were told to write tests without sufficient guidance, support and – crucially – there were few consequences for writing bad test code, as the testers would scuttle out from their partition, produce a dustpan and broom and proceed to clear up after the developers.

The result was that we had a huge amount of test cases that provided very little value – probably negative value, in fact. The maintenance cost alone was huge. Furthermore, running the main test suite took the best part of 10 minutes with ~6000 tests. It should've taken 6 seconds. 20 if I'm being very generous.

## Templates of Failure
How did this state of affairs occur? Well, people were asked to write tests, but nobody knew much about it and few people took an active interest.

Person A wrote their feature and attempted to write some tests. After a touch of cursory reading, Person A wrote some tests and bathed in the green glow of the NUnit GUI's progress bar. However, they didn't really fully grasp what they were doing and, as time was pressing on, were keen to finish the task and move on to the next one. 

Person B – a programmer of similar experience when it came to testing - looked at what Person A had done. "That looks like the done thing!", they cried while blithely repeating all of Person A's mistakes and probably throwing in a couple of new ones, too.

This attitude is very common in companies. The first rule of code is that, once it's checked in, it instantly becomes an order of magnitude harder to modify, correct and improve. Code hardens like concrete. The second rule of code is that other programmers will often use your code for reference, no matter the quality. Time is finite. If a programmer sees code that _seems_ to do the job and it is relevant to the problem they're trying to solve, it's fairly common that your shitty code becomes their shitty code. Anti-patterns propagate quickly. One by one, _they just started copying it_. 

What I'm trying to say is that, if shitty code is checked in, it can quickly become the de facto standard – a rigorously applied template of failure. The more alien the topic is, the more likely a developer is to engage in such behaviour.

## Slow down and think!
The reason I am saying this is that, at Realtime Worlds, the worst style of test code was the most prevalent, oft-aped and blindly repeated. People wanted to get their features in and understood neither the value nor the pitfalls of automated testing, as they received insufficient training or had no interest in it. Developers didn't stop to think about what automated testing _is_ or what it's _for_. We had thousands upon thousands of lines of largely worthless code that had to be maintained. It took a long time to change things. 

In the examples I gave, neither of those tests is useful. They prove very little, they're hard to understand and difficult to maintain. The class under test is a mathematical one, too! Matrices have no dependencies. It doesn't get much simpler than testing classes that have no dependencies.

## Automated Testing is a Skill
The key is to change how you think about testing. Testing is just like any other aspect of programming – if you want to reap the reward, you need to put in the effort to build up your skills. It's a gradual ramp from "derp, I know nothing" up to the finer points of test data builders, different testing styles and whatnot.

It's not just a case of including a framework, clattering out a few test methods and learning to click the buttons on the test runner GUI. If you don't have the time to take it seriously and treat your test code as a first-class citizen, it's probably not going to go particularly well. 

## The Bad News
If you do it badly on a large scale, here's a list of just _some_ of the issues you can encounter:

  * The tests do nothing to prove that your software functions correctly 
  * The tests only prove that the ‘happy path' works – unexpected data causes failures in production 
  * Some tests are not deterministic (they will periodically fail) 
  * Developers do not trust the tests. Test failures are routinely ignored 
  * Tests can have side-effects (so running test 3 after test 10 could cause a failure, but not vice-versa) 
  * Developers don't understand what certain tests are trying to prove 
  * Even if developers understand the purpose of a test, it's time-consuming to debug a failure as the test code is too convoluted 
  * The tests run extremely slowly, retarding productivity 
  * The tests routinely break (fail to compile or don't pass when executed) when minor changes are made to production code. Developers throw their hands in the air and delete the tests rather than fix them. 
  * Developers cannot test swathes of production code, as it has intractable, unbreakable dependencies 
  * Developers tend to repeat huge amounts of code when writing tests. 
  * Tests pass when the production code is broken, as the test code apes the class under test. 
  * Tests pass regardless of the implementation being correct. I.e. the test is bugged, usually due to (incorrectly) performing calculations in the test code itself. 

## The Good News
The vast majority of these problems can be tamed by applying a handful of principles, which I will outline in further posts.