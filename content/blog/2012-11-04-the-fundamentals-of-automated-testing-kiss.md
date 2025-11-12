+++
title = "The fundamentals of unit testing: KISS"
tags = ["fundamentals of unit testing", "testing", "tips"]
path = "/blog/2012/11/04/the-fundamentals-of-automated-testing-kiss.html"
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

KISS, ([Keep it Simple, Stupid](http://en.wikipedia.org/wiki/KISS_principle)) is a guiding principle in software engineering and it's of vital importance when writing tests. Tests should be straightforward and contain as little logic as possible. 

I know from painful experience that trying to do something overly 'clever' in a test is a recipe for disaster.

## Control Flow / Extra Logic in Tests

The moment you start changing the flow of a test based on some condition, you are setting yourself up for a fall. Think about it: we test a particular unit of production code because its logic may be flawed. If the test that validates the production code tends towards the same level of complexity, there is a distinct and real risk that the test code will also contain errors.

Here's a real example of a bad test that contains error-prone logic (please ignore the potential floating point comparison issues... I'll touch on that later):

```cs
[Test]  
public void IdentityTest()  
{  
  var m = Mtx4f.Identity;

  for(int r = 0; r < 4; ++r) // potential error; looping  
  {  
    for(int c = 0; c < 4; ++c) // potential error; looping 
    {
      if(r != c) // potential error; logical test / branching
      {  
        Assert.AreEqual(m[r, c], 0.0f);
      }  
      else // potential error; logical test / branching  
      {  
        Assert.AreEqual(m[r, c], 1.0f);  
      }  
    }  
  }  
}
```

Off the top of my head, here's a list of gripes I have: The test loops _and_ branches in a totally unnecessary fashion. It's easy to get an r or a c mixed up, just as it's simple to make an if/else mistake. The assert branching is particularly concerning. There's a few extra variables in the mix too, so there's more balls in the air, so to speak. 

In addition to the potential for logical errors, I can't just look at the code and say, "row 3, column 2 of the matrix should have <x> value". As a result, the test has been obfuscated, because I have to understand & walk through the execution of an algorithm to determine what the result should be. In this case, the test code is actually _much more_ complicated than the production code it is testing – a red flag if I've ever seen one.

Would it really have hurt so much to validate the 16 elements manually? We're talking about 16 lines of code versus 12 or 13 lines of _complicated_ code- it's not the end of the world, and it's not often you have to write such verbose code.

Here's two alternative tests that do the same thing in a simpler way:

```cs
[Test]  
public void IdentityTest()  
{  
 var i = Mtx4f.Identity;

 // Row 0  
 Assert.That(i[0,0], Is.EqualTo(1f));  
 Assert.That(i[0,1], Is.EqualTo(0f));  
 Assert.That(i[0,2], Is.EqualTo(0f));  
 Assert.That(i[0,3], Is.EqualTo(0f));

 // Row 1  
 Assert.That(i[1,0], Is.EqualTo(0f));  
 Assert.That(i[1,1], Is.EqualTo(1f));  
 Assert.That(i[1,2], Is.EqualTo(0f));  
 Assert.That(i[1,3], Is.EqualTo(0f));

 // Row 2  
 Assert.That(i[2,0], Is.EqualTo(0f));  
 Assert.That(i[2,1], Is.EqualTo(0f));  
 Assert.That(i[2,2], Is.EqualTo(1f));  
 Assert.That(i[2,3], Is.EqualTo(0f));

 // Row 3  
 Assert.That(i[3,0], Is.EqualTo(0f));  
 Assert.That(i[3,1], Is.EqualTo(0f));  
 Assert.That(i[3,2], Is.EqualTo(0f));  
 Assert.That(i[3,3], Is.EqualTo(1f));  
}
```

This one is fairly verbose, has some scope for errors (row & column accessors are very easy to typo and/or transpose) and will soon get cumbersome if you have to write multiple tests. To work around the verbosity, I would probably go with something more like this:

```cs
[Test]  
public void IdentityTest()  
{  
 // Arrange  
 var identity = Mtx4f.Identity;  
 var expected = Matrix(1, 0, 0, 0,  
 0, 1, 0, 0,  
 0, 0, 1, 0,  
 0, 0, 0, 1);

 // Act & Assert  
 Assert. That(identity, Is.EqualTo(expected));  
}
```

**Note**: the second test assumes that there is an equals implementation for Mtx4f and it is well-tested. In an ideal world we'd only ever use the unit of code we're testing, but I'll often compromise. 

Depending on whether you think it's a good idea to ever do a direct floating point comparison without a specified tolerance value (hint: it's generally a bad idea) _and_ whether you think having an equals implementation for matrices is good design, either of these choices may be deemed unacceptable. 

I'd personally go for a third way™: write a testing extension that checks two matrices with a specified tolerance value.
Something like this would do it:

```cs
static void AssertEqualsWithinTolerance(
  Mtx4f a, Mtx4f b, float tolerance)
```

Add it to a testing helpers namespace and write a few tests for it. You can also extend some test runners to make it read more idiomatically. It's important to write tests for utility / helper test code, as anything that uses it is making the assumption that it is correct and trustworthy.

## Be as Declarative as Possible

Leading on from this, I also advocate being as declarative as possible. Basically, in test code, we should endeavour to 
say _what_ the result should be, not _how_ to calculate it. Do your best to stick to this rule of thumb and it'll save 
your life a thousand times over. I'll talk about this more when I cover 
"[Don't ape production code in tests](@/blog/2012-11-12-the-fundamentals-of-automated-testing-tests-shouldnt-ape-the-production-code.md)" 
in a future post.

## Test Code is Simple Code

I sometimes hear folk griping about how much test code they have to write. However, writing code is generally not the bottleneck in productivity. We spend more time thinking, testing and debugging than we do actually _writing_ code. Furthermore, the simpler the code is in terms of its content, the more of it we can write and the easier it is to maintain. 

I say this because, for me, test code falls into the "simple" category. I know for a fact that I can bang out test code in a fraction of the time it takes to write production code. Why is that? Well, it's because the test code is doing comparatively little of note. I don't have to tweak loop boundary conditions, fix break/continue bugs, remedy branching errors and the like. 

That's not to say that test code doesn't have its own nuances and pitfalls, but once you internalise the rules to writing good tests, things go much more quickly. Most of the time sunk into tests tends to be invested in making them maintainable - comparatively little time is spent in fixing logical errors. 

## KISS on a Larger Scale

Sometimes it seems like a good idea to do something 'clever' to reduce the amount of testing work we have to do. However, any time you hit upon such a scheme, take a step back and think about it carefully. I remember the early days of my time at RTW where I attempted to write a clone test that would find all types that subclassed a type T, clone them, then loop through their properties, checking for equality. It worked first time. I thought I must be some kind of genius. 

It backfired horribly, though. As new types were added, the test broke repeatedly. Due to all of the hoop jumping I was doing to discover and map the types, the test code was barely understandable and, due to its brittle nature, represented a maintenance risk. Debugging a failure was as clear as mud.

Ultimately, I deleted it and replaced it with simple, individual tests. They worked fine and were written inside a 
couple of hours -- far less time than I spent dicking around trying to make a 'clever' solution work. 

Oh and the simple solution never once broke.