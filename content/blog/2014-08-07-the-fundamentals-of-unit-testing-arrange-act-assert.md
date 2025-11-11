+++
title = "The fundamentals of unit testing: Arrange, Act, Assert"
tags = ["fundamentals of unit testing", "testing", "tips"]
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

"[Arrange, Act, Assert](http://c2.com/cgi/wiki?ArrangeActAssert)" (aka "AAA") is a very simple way to structure your tests – I thoroughly recommend it. It is especially helpful when learning the ropes.

For this post, I’ll use the following example test scenario: When a stack is empty, pushing an item increments the 
count to one (this example was previously discussed in 
[Narrow & focussed](@/blog/2012-10-25-the-fundamentals-of-automated-testing-narrow-focused.md), if you want 
more context)

```cs
[Test]  
public void pushing_an_item_onto_an_empty_stack_increments_count()  
{  
 // Arrange  
 var stack = new Stack<bool>(); 

 // Act  
 stack.Push(false); 

 // Assert  
 Assert.That(stack.Count, Is.EqualTo(1));  
}
```

Each ‘phase’ of the test happens in order and occurs precisely once. Arrange precedes Act, Act precedes Assert. I’ll go into a little more detail later as to why this is a useful property.

A brief description of each "A" follows.

## Arrange
To be able to put yourself in a position where you can invoke a method and check that the result was correct, you first need to able to put things into a ‘primed’ configuration. If you want to test that your pistol can shoot a tin can, then you’d probably need to set up the tin can at an appropriate range, load the weapon and take the safety off before you even think about firing.

This step is often referred to as the “Arrange” phase, as you’re arranging things prior to calling the method/function of interest.

In the stack example, the arrange phase would simply mean creating an empty stack. In more complicated scenarios, you will need to do more work to knock things into shape.

## Act
The action is the main bit of the show. It’s the bit the test is interested in, whether because calling a method or function returns a result that can be directly scrutinised, or because calling it causes a side-effect that can be observed (mutation of state, call to another class, an event being raised etc). 

This is often called the “Act” phase.

In the empty stack example, the “Act” phase occurs when Push() is called, as this is the ‘interesting’ call in the test – the one that exercises the unit of code under test.

## Assert
The assertion is the part that ensures that your expectations are met. You can cobble objects together and call any number of methods, but unless you actually check a _meaningful_ result, there’s little point in it. Without a good assertion, the best you can do is prove that the unit of code under test hasn’t crashed – there’s very little value in this.

This step is often called the “Assert” phase.

In the stack example, the “Assert” phase occurs when the Count property is checked against our expectation.

## Why use this structure?
Put short, it’s a rigid template that serves as an excellent code smell detector. When your test code starts to deviate from being simple (e.g. it has multiple interleaved actions and asserts), it tends to break this template in a way that is very obvious. 

E.g., once you’ve entered the Assert phase, you should only be verifying results, not performing actions on the class under test. If this occurs, something is likely iffy.

If we return to the 
[Narrow & focussed](@/blog/2012-10-25-the-fundamentals-of-automated-testing-narrow-focused.md) post, you’ll 
see that the examples of bad tests cannot follow the AAA scaffolding, as they quickly repeat phases, mixing arranges, 
acts and asserts all over the place.

Take this example of a bad test that I’ve lifted from that post (I’ve shortened a bit), for example:

```cs
[Test]  
public void BadPushPopTest()  
{  
 var stack = new Stack<int>();  
 Assert.That(stack.Count, Is.EqualTo(0)); 

 stack.Push(1);  
 Assert.That(stack.Count, Is.EqualTo(1)); 

 int popped = stack.Pop();  
 Assert.That(popped, Is.EqualTo(1));  
 Assert.That(stack.Count, Is.EqualTo(0));  
}
```

Let’s try and structure it using the Arrange, Act, Assert comments and see how it holds up:

```cs
[Test]  
public void BadPushPopTest()  
{  
 // Arrange  
 var stack = new Stack<int>();  
 Assert.That(stack.Count, Is.EqualTo(0)); // Warning: asserting in the Arrange phase**!

 // Act  
 stack.Push(1); 

 // Assert
 Assert.That(stack.Count, Is.EqualTo(1));

 int popped = stack.Pop(); // Warning: action in the Assert phase**!  
 Assert.That(popped, Is.EqualTo(1)); // Warning: why are we asserting again?  
 Assert.That(stack.Count, Is.EqualTo(0)); // Warning: and again...  
}
```

It doesn’t work, because the test is not focused enough. It would be very difficult (probably impossible) to whip this into a reasonable AAA structure. If a test does not fit into the AAA structure, it’s almost always a warning sign that the test needs split into multiple tests. 

I can’t think of a single unit test I’ve written that legitimately violated the AAA scaffolding.