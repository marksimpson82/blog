+++
title = "The fundamentals of unit testing: Repeatable"
tags = ["fundamentals of unit testing", "testing", "tips"]
path = "/blog/2012/11/04/the-fundamentals-of-automated-testing-repeatable.html"
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

The main purpose of automated testing is to highlight problems with correctness in production code. When a test fails, it means, "something is wrong here; we have a bug in our production code!" I'm sorry about your canary. It died a valiant death.

## Tests Should be Repeatable

... so what do I mean when I say that tests should be repeatable? By repeatable, I mean each test can be executed an arbitrary number of times without observing a change in the test results. If a developer can run a unit test 100 times in a row and get two or more distinct results **without** altering any production/test code, the test is not repeatable. 

## Why Should I Care?

If a unit test cannot yield the same result with every single test run, then it is non-deterministic and untrustworthy. 

An unreliable, flaky test is analogous to a car alarm that has been going off for two days. There _might_ be something wrong, but nobody will pay any attention to it. 

Most people who've worked with large test suites will have experienced a particular situation from time to time – the case where a handful of the tests intermittently fail. Developers quickly recognise the problematic test name(s) and exclaim, "these tests sometimes fail for no reason". The next step is to click the "rebuild" button on the continuous integration server. Without changing a thing, the tests pass. Hooray! If you joined in with the cheering, then please punch yourself in the face (it was a ruse).

When folk mindlessly click the "rebuild" button, we've lost. At this juncture, the developers don't trust the tests. Remember when I said that the purpose of tests is to act as a canary in the mine? Well, the canary died and, rather than saying "everyone out of the shaft!" their first reaction was to send in more, as perhaps the first one had asthma or died of natural causes. If people merely gloss over the root cause of the failure and try to make the failure "go away", this signals a collective shift into [NOMFuP](http://www.urbandictionary.com/define.php?term=NOMFup)-land. If you're unfamiliar with NOMFuP, I recommend watching [The Thick of It](http://uk.imdb.com/title/tt0459159/).

> **[Malcolm Tucker](http://uk.imdb.com/name/nm0134922/)**: NOMFuP.  
> **[Jamie](http://uk.imdb.com/name/nm0383467/)**: Eh?  
> **[Malcolm Tucker](http://uk.imdb.com/name/nm0134922/)**: NOMFuP. N-O-M-F-P. Not My Fucking Problem. 

## Causes

Some of the causes of an unreliable test can be found on the previously-blogged 
[Atomic](@/blog/2012-11-02-the-fundamentals-of-automated-testing-atomic.md) post (basically: global/static
state and environment dependencies). 

However, there are some other issues that can cause tests to fail.

### Threading

Any kind of unit test involving threading should set alarm bells ringing. Threading tests immediately take a dependency on the environment, as thread interleaving is non-deterministic. As such, any test involving threads can highlight race conditions amongst other things. 

I.e. if threading is used in tests, that test is by default not a unit test. You should note that neither the test nor the class under test should be creating threads.

While there's nothing inherently wrong about using threads in integration/functional tests, careful decisions have to be made about how to make each test robust. Threading is notoriously easy to get wrong and introduces the scope for several classes of bugs you won't see in single-threaded code.

Here's an example of a test that spins up a thread (again, please do not use this as an example of how to do things, as it's flawed in several ways). I've highlighted the lines in the test body that involve threading concerns:

```cs
[Test]  
public void TestLocking()  
{  
 var ptr = Memory.Alloc(128, "test", "Memory");  
 Thread t2 = new Thread(() => Memory.MemSet(ptr, 6, 128));  
 t2.Start();

 while (t2.IsAlive)  
 {  
 Thread.Sleep(10);  
 }

 Memory.Free(ptr);  
}
```

Ignoring the non-descriptive name and the lack of a meaningful assert, this is a fairly simple test that seems to be checking that a memory system can allocate and de-allocate across different threads, yet the majority of the code is dealing with threading concerns. Threaded tests run the risk of race conditions, re-entrancy problems, deadlock, livelock and all of the rest. Also, the more lines of imperative code added to tests, the more risky it is that a bug will be introduced _in the test itself_. 

The main reason to avoid threading in unit tests is that threading is dependent on the machine configuration. Microsoft discovered the vast majority of its Windows threading bugs when running integration/end to end tests on an eight core machine. However, the same tests passed without an issue on machines with one or two cores. Bearing this in mind, do you _really_ want to play Russian roulette with your unit tests? I don't. 

As I said, I'm not trying to entirely dissuade folk from testing threaded code, but to be aware that they're not unit tests and that special care and consideration must be taken when doing so. 

### Timing

Timing is related to threading, but typically manifests itself as the test code having to work around timing issues present in the class under test (as opposed to spinning up threads in the test code). 

Here's an example (again, please don't etc. and so forth – it's not great code): 

```cs
[Test]  
public void LoadRequestTest()  
{  
 Command command = new Command(
   PipeCodes.Loader_PathFile, etc ..., null);
 ResourceSystem.commandQueue.ExternalEnqueue(command);

 int count = 0;  
 while ((command.OpCode != OpCodes.Error) &&  
 (count < 100))  
 {  
 Thread.Sleep(10); // Why 10?  
 count++;  
 }

 Assert.AreEqual(OpCodes.Error, command.OpCode);  
}
```

The name isn't very helpful, but let's just focus on the timing concerns. Notice that there is no sign of threading. The production code is spinning up threads under the hood, though. Aside from the difficulty understanding the intent of the test, the test relies on the magic number of 10 milliseconds. Presumably something (I'm not quite sure what) takes time to process, so the loop has 100 iterations in which to succeed, and a value to wait after each pass of the loop. 

Not only does this test have readability issues and a load of logic cooked in, but it is sensitive to timing issues. Just because 10 milliseconds was an adequate sleep value on one PC doesn't mean it will work on another. Worse still, if functionality that this class relies on changes or the machine is overloaded when the test runs, the test may fail. I've seen this multiple times when flaky tests run fine on developer machines, but fail on CI server(s) because they're under more load. Furthermore, this test is running-in-molasses _slooooooooow_ due to the Sleep() call.

## Alternatives

There are a few ways to improve these problems or eliminate them entirely in unit test situations. 

### Don't unit test threaded code

The first and simplest suggestion is to avoid writing unit tests for threaded or timing-sensitive code. If you are stuck with inflexible threading model and cannot change it, write integration tests with plenty of timing slack, instead. If you can change the code, read on. 

### Hollywood principle

The first improvement is to alter the class API to follow the [asynchronous invocation](http://shiman.wordpress.com/2008/09/11/c-net-delegates-asynchronous-invocation-endinvoke-method/) model or something similar. Instead of waiting and polling, you can get a callback or block until the operation is completed. While this doesn't solve the fact that some calls will occur on different threads, it does mean that you can run tests without needing to poll for completion. 

### Decouple the threading model

The second improvement is to decouple the threading model from the system that uses it. This effectively allows a developer to force the system into a single threaded mode for unit testing. While this will result in any threading issues going undiscovered in the unit tests, these bugs should be covered by complementary integration and end to end tests anyway. 

I used this approach to thread resource streaming in a Unity3d project and it worked like a charm. Not only was the code testable, it was doubly useful as, any time errors cropped up, I could just force the system into single threaded mode and (largely) eliminate threading from my enquiries.