+++
title = "The fundamentals of unit testing: Narrow & Focused"
tags = ["fundamentals of unit testing", "testing", "tips"]
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

When it comes to writing unit tests, it pays to be _specific_. 

If you have a narrow & focused test, it will...

* be easy to make a descriptive name for the test 
* perform the bare minimum of work required to achieve its goal. 
* be easy to understand 
* be easy to maintain 
* execute in a shorter period of time 

## An unfocused example

To give you an idea of what an unfocused test looks like, consider the following (and yes, I've seen plenty of these, both in professional [RTW] & open source code):

```cs
[Test]  
public void StackTestA()  
{  
 var stack = new Stack<int>();  
 Assert.That(stack.Count, Is.EqualTo(0)); 

 stack.Push(1);  
 Assert.That(stack.Count, Is.EqualTo(1)); 

 stack.Push(2);  
 Assert.That(stack.Count, Is.EqualTo(2)); 

 var p = stack.Peek();  
 Assert.That(p, Is.EqualTo(2);  
  
 stack.Push(3);  
 Assert.That(stack.Count, Is.EqualTo(3));  
  
 stack.Pop();  
 Assert.That(stack.Count, Is.EqualTo(2));  
  
 bool c0 = stack.Contains(1);  
 Assert.That(c0, Is.True);  
  
 bool c1 = stack.Contains(10000);  
 Assert.That(c1, Is.False);  
  
 stack.Push(3);  
 Assert.That(stack.Count, Is.EqualTo(3)); 

 int popped = stack.Pop();  
 Assert.That(popped, Is.EqualTo(3));  
 Assert.That(stack.Count, Is.EqualTo(2));  
}
```

Can you spot the problems? 

Firstly, the name is vague and doesn't tell us anything about what the test is doing. No mention is made of the state of the unit of code under test, the actions performed or the expectations. 

As it happens, we can't give this test a good name, because it's a total scattergun effort. Since it does about 7 different things, any attempt to name it will result in a spiel resembling a 9 year old boy's attempts to describe his summer holidays. 

> I went to the seaside and I had an ice cream and then I went in the sea and then I saw a seagull and then I was tired so we had chips then we went home. It was good!

If we break it down, we can see numerous things being tested. 

  * The initial state of the class after the constructor runs 
  * Pushing an item onto the stack increases the count 
  * Popping an item off the stack decreases the count 
  * Popping an item off the stack returns the item that was previously at the top of the stack 
  * Peeking returns the item that is at the top of the stack 
  * Contains returns true when an item is contained in the stack 
  * Contains returns false when an item is not contained in the stack 

## A minor improvement

OK, so .. there's a lot of things happening and we want to simplify matters. The obvious thing is to split each of these situations / asserts into their own tests. 

A developer then creates the following:

```cs
[Test]  
public void PushPopTest()  
{  
 var stack = new Stack<int>();  
 Assert.That(stack.Count, Is.EqualTo(0)); 

 stack.Push(1);  
 Assert.That(stack.Count, Is.EqualTo(1)); 

 stack.Push(2);  
 Assert.That(stack.Count, Is.EqualTo(2)); 

 stack.Push(3);  
 Assert.That(stack.Count, Is.EqualTo(3)); 

 int popped = stack.Pop();  
 Assert.That(popped, Is.EqualTo(3));  
 Assert.That(stack.Count, Is.EqualTo(2));  
}
```

This is better, but it's still quite vague; you can't really describe what the test is doing, the behaviour it is testing or the expectation. 

Is it testing the relationship between pushing/popping and the count changing? Is it more interested in the item being popped off the stack? What about the initial state of the object? Hmm!

What can we do to improve matters? Well, let's get specific.

## Choosing a descriptive test name

This is the most important thing. To name a test, you need three things. You need to know what the situation is, the action performed and the expected result. 

In <**x**> situation, when I do <**y**>, <**z**> should happen. For example, "when there are no items on the stack, calling Push() with an item causes the count to be incremented by one". 

Notice that this name talks about **one** specific situation, **one** action and **one** expectation. A well-named test means a developer doesn't even need to read the method body's code to understand the intent behind the test. This is crucial. If you can't understand what your test is proving, how can you expect someone else to make sense of it? If you cannot think of a good name for the test, it is generally a red flag.

Once you have a good understanding of what your test is proving and you've chosen a name, we can move on to the nuts and bolts of writing the test.

## Writing the test code

Again, our example is:

in a situation where **<The stack is empty>** and **<An item is pushed>**, then **<The count is incremented to one>**.

Now let's translate the sentence into code by writing a test for this single unit and nothing else.

### A focused test

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

Ta-da! It's laser beam focused. You can clearly see the arrange, act and assert phases match the name of the test. There is no noise, incidental setup code, spurious actions or orthogonal assertions. It does exactly what is needed and no more. 

Furthermore, if this test ever fails, you probably won't even go as far as attaching a debugger as it's so clean and simple. Hell's teeth, I could read the failure message in the console runner and tell you what it's _meant_ to be proving. My mum could, too. 

Finally, if the stack's behaviour is changed down the road, this test will probably still pass, as it is only asserting against a very specific bit of state (the count). The less you touch in a test (be it arranging, acting or asserting), the smaller the surface area of the test. The smaller the surface area, the less likely it is to break.

**Note**: I would normally create a factory method to construct the stack to provide some level of insulation from constructor changes, but I don't want to pollute an already rather-longer-than-expected post 

## Lots of tests!

Once your tests reach this level of simplicity and your fully embrace the <**situation**>, <**action**>, <**expectation**> style of thinking / naming, it becomes very easy to dream up new scenarios. Each scenario becomes a separate, focused, stand-alone test.

Off the top of my head:

* When a stack is created, the count is zero 
* When a stack is empty, popping causes an exception to be thrown 
* When a stack has items, peeking returns the top item 
* When a stack has items, peeking does not remove the item from the stack 
* When a stack has items, popping decrements the count 
* When a stack has items, popping returns the item that was previously at the top of the stack 
* When a stack has a specific item, calling contains with that item should return true 
* When a stack does not have a specific item, calling contains with that item should return false 
* etc.