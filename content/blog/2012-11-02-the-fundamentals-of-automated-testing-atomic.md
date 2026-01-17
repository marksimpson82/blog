+++
title = "The fundamentals of unit testing: Atomic"
tags = ["fundamentals of unit testing", "testing", "tips"]
path = "/blog/2012/11/02/the-fundamentals-of-automated-testing-atomic.html"
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

Every single unit test you write should be atomic. 

## A definition

Atomic tests are order-independent, relying on and causing no side effects. They neither rely on nor alter shared state; they do not mutate their environment. If a test run involves 2, 10, 100 or 1,000,000 tests, the tests should be able to be executed in any order. If one legitimately fails because a bug has been introduced in the production code, it shouldn't have a domino effect. 

For example, if we have 3 tests named A, B and C, we should be able to run these tests in _any_ order. For a tiny set of 3 tests, there are already 6 ways of arranging the order of execution: ABC, ACB, BAC, BCA, CAB, CBA. If the order ABC is fine, but the order BAC causes test C to fail, then one of the tests is non-atomic. 

Put short, a test should be built up and torn down cleanly, leaving no trace of the fact that it has been executed. 

## Why is this important?

A good automated test has a descriptive name, is implemented using straightforward code and leads us to the cause of the failure without much hassle. When dealing with well written atomic tests, at the very worst, diagnosing the cause of a failure should be a simple debugging job.

However, if non-atomic tests create knock-on effects it introduces a significant maintenance risk, as to diagnose failures, we must understand the whole picture. Instead of just inspecting the local state that exists prior to executing the failing test, we have to start delving into environmental differences (machine configuration, file systems) and [AppDomain](http://blogs.msdn.com/b/cbrumme/archive/2003/04/15/51317.aspx) issues (typically global / static state).

While most test failures caused by a lack of atomicity are localised (e.g. tests confined to one fixture start to fail), I've personally witnessed a system under test causing hundreds of test failures spanning multiple (seemingly unrelated) fixtures.

Furthermore, if failures cannot be reliably reproduced, it undermines the trust in those tests. People won't pay attention to them, even if the failures are legitimate. The moment developers see a red build and, without even thinking about it, click the "rebuild" button, you're entering the world of [NOMFUP](http://www.urbandictionary.com/define.php?term=NOMFup). 

## Tell Tale Signs

How can you tell that you have non-atomic tests lurking in your codebase? 

1. Test runners don't always find and run tests in the same order - they are often loaded in an arbitrary order. A good example of this phenomenon is the disparity between ReSharper and NUnit. They both execute tests in different orders (or they did last time I checked with a large sample set). If different results can be obtained by running the same tests using different runners, it's probably caused by non-atomic tests.

1. Running your entire test suite or a subset of it with the **same instance** of the test runner may cause failures the Nth time around. E.g. in .NET land: open the NUnit GUI, load your tests and then repeatedly run the tests.

**Note**: There is a combinatorial explosion involved with order dependence, so these two signs aren't guaranteed to present themselves.. The best defence is to write production & test code bearing a few things in mind.

## Cause: Static State in Production Code

The biggest offender by far is static state mutated / read by the _production_ code. For most intents and purposes, static is just "global" by another name.

If we have a class under test like the following (please note: do not write code like this!):

```cs
public class ModelLoader  
{  
 public Model Load(string xml)  
 {
 ... // some processing occurs then...  
 var handle = MemoryManager.Allocate(numVertices * vertexSize); // a static call  
 }  
}
```

... and the static dependency:

```cs
public static class MemoryManager  
{  
 private static MemoryPool m_memoryPool;

 public static void Init()  
 {  
 // does initialisation stuff.  
 m_memoryPool = new MemoryPool();  
 }

 public static MemoryHandle Allocate(long numBytes)  
 {  
 // this will crash if Init wasn't called  
 return m_memoryPool.DoSomething();  
 }

 public static void Quit()  
 {  
 // poor man's Dispose()  
 }
```

... then `ModelLoader` has an _implicit_ dependency on the `MemoryManager`. It's implicit because there is nothing in the public API to say that this static class `MemoryManager` is used, let alone that it must be initialised if we want to use the `ModelLoader`. As Misko says, [Singletons are pathological liars](http://misko.hevery.com/2008/08/17/singletons-are-pathological-liars/). 

As a result, if we forget to call the static `Init()` or `Quit()` methods, the state mutations caused by one test will bleed into the next. 

Here's the (horribly non-atomic) test code:

```cs
[TestFixture]  
public class StaticStateHurtsMyBrainTests  
{  
  [Test]  
  public void loading_simple_model_xml_returns_valid_model()  
  {  
    // Arrange  
    MemoryManager.Init(); // static state initialised here!  
    var modelLoader = new ModelLoader();

    // Act. Our class under test depends on implicit static state contained in MemoryManager  
    var loadedModel = modelLoader.Load("<Model Name = ... etc ");

    // Assert  
    Assert.That(...) // Note: we forgot to call MemoryManager.Quit()  
  }

  [Test]  
  public void loading_model_with_positions_and_uvs_returns_valid_model()  
  {  
    // Arrange. Uh oh, we forgot to call MemoryManager.Init()  
    var modelLoader = new ModelLoader();
 
    // Act. MemoryManager isn't initialised; test will fail here. Or will it?!  
    var loadedModel = modelLoader.Load("<Model Name = ... etc");
 
    // Assert  
    Assert.That( // etc.  
  }  
}
``` 

We're now in a world of pain. Depending on the order the tests are run _and_ whether individual tests pass or fail, we may obtain different results. Can you see why? The author of the first test has correctly ascertained that the nasty (hidden) MemoryManager dependency must be initialised, but doesn't shut it down correctly. Since the MemoryManager is a static class, its state remains in the AppDomain from test to test. As a result, the second test will possibly pass, but only if it runs after the first. If the order is switched, we'll definitely have a minimum of a single failure. These tests are non-atomic.

## Fix: Remove Static State

To solve this problem, the static state should be replaced with instance-based construction and any functionality that needs access to it should explicitly ask for it via the constructor or other means, like so:

```cs
public class ModelLoader  
{  
  private MemoryManager m_memoryManager;  
   
  public ModelLoader(MemoryManager memoryManager)  
  {  
    m_memoryManager = memoryManager;  
  }  
   
  public Model Load(string xmlString)  
  {  
    ... // some processing occurs .. then  
    m_memoryManager.Allocate(numVertices * vertexSize);  
  }  
}

public class MemoryManager // probably implement IDisposable too, but it's just an example so...  
{  
  private MemoryPool m_memoryPool;
 
  public MemoryManager()  
  {  
    m_memoryPool = new MemoryPool();  
  }
 
  public MemoryHandle Allocate(long numBytes)  
  {  
    return m_memoryPool.DoSomething(numBytes);  
  }
}
```

This greatly simplifies the complexity by making dependencies explicit, limiting access and removing the carried over state. We have ensured that the ModelLoader has a properly constructed MemoryManager dependency and that it can be constructed and thrown away without causing side effects. 

Do not simply refactor the test code such that it calls static methods before/after each test is run. This is just a bandage over a horrible API. Static state is a bit like playing whackamole – you can thrash most of it into shape, but there's always a point where it becomes too much to handle. 

Tests are microcosms of real usage - if something is hard to use in a test, it is hard to use, period. Unless you _really_ have a need for a static type and you are well-versed in the risks, avoid it.

## Cause: Test Depends on Filesystem

Any test that is dependent on its environment is an integration test. The most common way the environment manifests itself is when dealing with the file system. The filesystem is the filesystem. It persists before, during and after a test run, so it stands to reason that modifying it can cause knock-on effects.

```cs
[TestFixture]  
public class OrderDependentTests  
{  
  private const string Filename = "myfile.txt";
 
  [Test]  
  public void when_the_file_exists_constructor_loads_the_file_contents()  
  {  
    // Arrange  
    File.Create(Filename);  
    // imagine this opened the file and wrote something in
    AddThreeElementsToFile(Filename); 
   
    // Act  
    var systemUnderTest = new TypeLoader(Filename);
   
    // Assert  
    Assert.That(systemUnderTest.LoadedTypes, 
      Has.Count.EqualTo(3));  
  }
 
  [Test]  
  public void when_file_exists_that_contains_only_comments_constructor_doesnt_load_anything()  
  {  
    // Arrange  
    // this requires the file to exist! Does it? Maybe.
    AddCommentToFile(Filename); 
   
    // Act  
    var systemUnderTest = new TypeLoader(Filename);
   
    // Assert  
    Assert.That(systemUnderTest.LoadedTypes, 
      Has.Count.EqualTo(0));  
  }
 
  [Test]  
  public void when_file_does_not_exist_constructor_doesnt_load_anything()  
  {  
    // Arrange  
    // what happens here if the previous test(s) didn't run yet?
    File.Delete(Filename); 
   
    // Act  
    var systemUnderTest = new TypeLoader(Filename);
   
    // Assert  
    Assert.That(systemUnderTest.LoadedTypes, 
      Has.Count.EqualTo(0));  
  }  
}
```

Firstly, you should note that these tests touch the file system and are really integration tests. Secondly, if these tests run in the order they're defined, they'll pass. However, if the order is mixed up, or the test that relies on the file existing is run in isolation, the test(s) will fail! 

## Fix: Don't Rely on the Filesystem

For unit tests, abstract the production code's file IO by at least one level. By this, I mean separate the loading & processing of files and their contents. You can still present file loading APIs to the user, but the guts of the implementation uses streams, allowing fast, in-memory unit testing for the more complicated ‘inner' code. 

I wrote a post about this a while back, so [take a look](@/blog/2009-11-26-avoiding-the-file-system.md).