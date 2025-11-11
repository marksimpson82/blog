---
id: 709
title: "The fundamentals of unit testing: Spring The Trap"
date: 2012-10-27T23:21:57+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=709
#permalink: /?p=709
tags:
  - fundamentals of unit testing
  - testing
  - tips
---
This post is [part of a series]({% post_url 2012-10-24-the-fundamentals-of-automated-testing-series %}) on unit testing.

This is a lesson I learned from the [Pragmatic Unit Testing](http://pragprog.com/book/utc2/pragmatic-unit-testing-in-c-with-nunit) book. Five years later and it’s still a tool that I frequently reach for – it’s simple and incredibly useful.

## Who tests the tests?

I’ve had a few long-winded and borderline philosophical discussions with colleagues in the past where the question is asked: “Who tests the tests?” In essence, how can we trust the tests to tell us that the production code is working correctly? Who’s to say the test isn’t bugged? If a test is bugged and erroneously passes, we have the worst of both worlds. We have a piece of (potentially) broken functionality and we have a test that is offering false assurances.

## Is this likely?

At first glance, it sounds a bit fanciful – I mean, what are the chances of writing a bad test? The truth is: It’s not a matter of if, it’s a matter of when. Everyone slips up now and again. Test code is code. Programmers habitually write incorrect code.

In my experience, it’s especially easy to write an incorrect test when you’re pre-occupied by something else (such as understanding & fixing a complicated bug) and aren’t really in the mood to question yourself before you check in and head home for a deserved nap. 

I’ll put it more pointedly: if the tests are written after the production code, how do you know that the test is correct? Think about it, if your workflow follows this pattern: “create method that does X, write test for method to make sure X is correct, the test passes”, how can you have confidence that the production code and its tests work? The test has never failed and, as a result, you are on the happy path. 

A common cause is copy-pasting an existing test and forgetting to change it to do something else by varying an argument or value. It happens. You now have two identical tests – one is misleadingly named and both pass.

## Reducing Errors
There’s two things you can do to increase the chance of a test being correct.

### Spring the Trap
Temporarily break the _production_ code to make sure the test detects the failure. Change the production code. Run the test. Does it pass? If it passed, the test is incorrect, as it failed to detect the bug. If it fails in the expected fashion, then your test is more likely to be correct. It doesn’t mean the test is 100% correct, but it certainly gives it more credibility.

Here’s a quick, contrived example:

```cs
public class ScratchPad // class under test  
{  
 private List<string> m_messages = new List<string>();

 public IEnumerable<string> Messages { get { return m_messages; } }  
  
 public void StoreMessage(string message)  
 {  
 m_messages.Add(message);  
 }  
} 
```

Here’s the test code:

```cs
[TestFixture]  
public class ScratchPadTests  
{  
 private ScratchPad CreateScratchPad()  
 {  
 return new ScratchPad();  
 }  
  
 [Test]  
 public void storing_message_adds_message_to_messages_list()  
 {  
 // Arrange  
 var scratchPad = CreateScratchPad();  
 var message = "Who moved my brie?"  
  
 // Act  
 scratchPad.StoreMessage(message);  
  
 // Assert  
 Assert.That(scratchPad.Messages.First(), Is.EqualTo(message))  
 }  
}
```

There’s nothing terribly interesting about this. The test passes, but how do we know the test is working correctly and not simply succeeding by coincidence?

Let’s spring the trap. To do this, we modify the class under test such that it no longer behaves in the way it should. The test we’re scrutinising is checking that the message is added to the messages IEnumerable. To make it fail, we need to comment out some code such that the message is not stored, like this:

```cs
public class ScratchPad  
{  
 private List<string> m_messages = new List<string>();

 public IEnumerable<string> Messages { get { return m_messages; } }  
  
 public void StoreMessage(string _message)  
 {  
 // this should now make the test fail.  
 // – intentionally broken! // m_messages.Add(message);  
 }  
}
```

The test now should fail, as the class under test no longer does the correct thing. If the test passes, the test is obviously not correct. 

### TDD

[Write your code test-first](http://en.wikipedia.org/wiki/Test-driven_development). I’m not going to go into much detail on this, as TDD is more of a _development_ style than a _testing_ style, and it’s a much bigger investment to commit to doing TDD-with-bells-on. 

The reason TDD reduces the chance of creating a bugged test is that the test is created first and **must** fail before you write the production code. If it does not fail, then you know the test is surely incorrect (how can a test pass when the functionality it’s testing is not yet implemented? It can’t!) 

There is a small step you can take to gain some of this benefit: write regression tests before fixing bugs. I.e. before you fix a bug, write the test that proves the bug exists (the test will fail on first run), then fix the bug and the test should go green. Again, this does not mean the test is perfect, but it is a much better state of affairs.