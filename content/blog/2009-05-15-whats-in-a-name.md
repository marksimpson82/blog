+++
title = "What's in a name?"
tags = ["testing", "tips"]
path = "/blog/2009/05/15/whats-in-a-name.html"
+++
One of the things I try to encourage is the careful selection of names. Just as self-documenting code is easier to read, so is a self-documenting test. As I have previously stated, unit testing is programming, too - you can apply the same good practices to tests.

On numerous occasions I've had to review some code and tests. I open the classes and find well-named, self-documenting, loving crafted, carefully designed code. Then I look at the test for that code and find that the same principles have not been applied to the tests. In fact, it's almost like the tests have been written by Evil Chuck, the programmer's alter-ego.

It's not uncommon to see something like the hugely descriptive and easy to read:

```cs
[Test]
public void TestMethodName()
{
...
}
```

.. the excellent

```cs
[Test]
public void TestMethodName4()
{
...
}
```

.. and the ubiquitous

```cs
[Test]
public void TestConstructor()
{
...
}
```

This is not a good state of affairs!

### Problems with badly named tests

Numerous problems exist with a name like "TestSomeMethod4B". Here are a selection of good reasons **not** to name your tests like this:

**Readability**  
It's not descriptive. In fact, it's totally obscure. It might as well not exist. What can you say about "TestSomeMethod4B"? Nothing much. Even if it is documented with a comment, it hinders readability in the IDE and the test runner. It's better to name something descriptively and without a comment than the other way around. That's not to say that comments and descriptions are redundant, but in most cases you don't need them if the test is descriptively named.

**Intent  
** It says absolutely nothing about the intent. It might be checking an exception is thrown, it might be checking a value is clamped to an accepted range of values. It might be doing nothing. To be able to decipher its intent, you have to read the code. Imagine if you couldn't understand the intent of any part or method of a program. How would you manage to break it up into understandable chunks? Answer: with great difficulty.

**Obfuscation  
** It defeats any kind of attempt to understand the state and thoroughness of the testing for that class as a whole. You cannot obtain an overview. You can't determine whether you've tested a method with 10 different invalid parameters or whether you've tested 10 different simple cases. Without good naming you are reduced to skimming the code while trying to remember too much. Just as well named subroutines aid comprehension of a larger problem, well-named tests give a good overview without forcing you to examine the contents of those tests.

**Redundant Prefix**  
In 99% of cases, if a public method is part of a test fixture and it has a [Test] attribute, it's a test. You don't need the Test prefix. It just hinders the skimming of the tests in alphabetic order. If you really insist on putting "Test" somewhere, put it at the end of the name. I personally wouldn't bother, though.

**What are you doing?**  
Finally and arguably most importantly, if you don't name your test well, there is a greater chance that **you don't know what the test is trying to achieve.** Would you start to write a production code method without any inkling as to what it did? Even if you did, would you then leave it in existence with the name "DoSomeStuff"?

Badly named tests are a smell. In my experience, well-named tests are nearly always attempting to prove something regardless of the quality of the test body. I cannot say the same for badly named tests.

Good intent and bad execution is often better than a tidy, aimless test. The former can be refactored into something useful, the latter requires decryption just to understand why it exists in the first place. In many cases, the test proves nothing.

If you write a test method and can't think of a name that describes the test before you write it, **stop**. Think about what you're trying to achieve, then choose a name that describes it adequately.

### How do I choose a good name?

First and foremost, what are you trying to prove with the test? Tests are meant to demonstrate something. They are meant to assert that some meaningful state is set, or some sort of interaction has taken place.

You need at least three pieces of information to name a test.

1. The thing that is being tested, such as a function, method or property (or a sequence of them)
2. The arguments/data/circumstance involved
3. The expected outcome. What is meant to happen? Be as explicit as you can.

That's it. That's all you need. I prefer to write mine in the format 1_2_3, but I'm sure everyone has their own personal style. As long as it's readable and consistent, I don't care.

### Compare and contrast

Here's a few examples of some good test names for a bounding box class.

* AddPoint_ValidPointOutsideExistingBounds_IncreasesBoundsToContainPoint()
* AddPoint_ValidPointInsideExistingBounds_DoesNothing()
* AddPoint_ValidPointOnEdgeOfBounds_DoesNothing()
* AddPoint_InvalidPointContainingNaN_DoesNothing()
* AddPoint_InvalidPointNull_ThrowsException()

Now compare those to equivalent, but badly named tests:

* TestAddPoint()
* TestAddPoint2()
* TestAddPoint3()
* TestAddPointBad()
* TestAddPointBad2()

One set is descriptive, easily graspable and allows you to skim the members list to get a good feel for the thoroughness of the tests. The other set of names tells us very little.

To those who say "I don't like long method names", I say, "It's a test. You write it once and read it hundreds of times. You never have to call into it from other code. Your screen is plenty wide enough to accomodate it." There is no reason to use short or bad test names 'just because'. I've yet to hear any meaningful criticism against giving test methods long names.

As the famous nerd quote goes (paraphrasing):

> "When I wrote this code, only God and I knew what I was doing. Now only God knows".

Just think about the poor sod who has to maintain your code in a couple of years. If you didn't know what the hell you were doing, what are they going to make of it?

### Other Advantages

If I have some good ideas about how to test something, or if I'm writing my tests before the production code, I will often use the 1_2_3 naming system to write out scores of empty test bodies. You may be surprised to see how effective this is.

You can plough through a group of methods in no time at all, thinking of all of the horrible things that could go wrong and writing them down. In no time at all, you can have a comprehensive test suite in waiting. The names are there, the intent is clear and you can proceed.

This is also a great tactic for division of labour when you're testing old code. Prototype the test bodies, check in the skeleton fixture(s) and multiple people can get cracking on different areas. I've done this quite successfully in the past.