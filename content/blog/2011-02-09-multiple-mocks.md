+++
title = "Multiple Mocks?"
tags = ["c#", "patterns", "testing", "tips"]
+++
This post was in response to a post on the [fragmental.tw blog](http://fragmental.tw/2010/12/14/one-mock-per-test-considered-not-awesome/) (the comments aren’t working for me, so I thought I’d post it here) which I read via [Roy Osherove](http://www.osherove.com/blog/2011/2/9/multiple-mocks-asserts-and-hidden-results.html).

Basically, the author was querying Roy Osherove’s rule of thumb that stated, “more than one mock per test is harmful”.

He then goes on to provide an example where one action has two identifiable/observable results, and two mocks are used.

**Figure 53b: Two Mocks (I’m so, so, sorry)**

[<img style="background-image: none; margin: 0px; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border: 0px;" title="image" src="https://defragdev.com/blog/images/2011/02/image_thumb.png" border="0" alt="image" width="244" height="244" />](https://defragdev.com/blog/images/2011/02/image.png)

Firstly, it was a rule of thumb (or at least I read it that way). I don’t see guidelines or so called “best practices” as edicts. You’re allowed to exercise discretionary thought and bend the rule when it doesn’t quite fit your situation.

It's a fair point, but I think you can have the best of both worlds. It’s perfectly possible to test two different bits of behaviour using two mocks, but while still keeping things readable with minimal code duplication.

* * *

## My general unit testing style

I believe in keeping my tests extremely simple. I usually call some methods to arrange, then I do something to act, then i assert. You can read one test method and see everything laid out in order without having to use a debugger or anything too taxing. It's annoying to have to go to SetUp methods to see what fields are set and which field corresponds to each test etc. However, when actions have multiple observable results, test "fixture as context" is often a good fit.

## Fixture as Context?

Yes, yes I know. It sounds a bit wanky. Sorry.

By “Fixture as Context”, I mean that if I have a complicated action that has multiple observable results, I create a test fixture that sets the context (i.e. wires up my object graph then performs the action before the asserts), then have multiple tests that assert on the result(s). The tests typically have nothing but an assert in the method body.

E.g.

```cs
public class when_updating_social_network_status  
{  
  private IFacebook m_facebook;  
  private ITwitter m_twitter;

  [SetUp]  
  public void before_each_test()  
  {  
    // wire up object graph and do the update stuff once  
  }

  [Test]  
  public void facebook_is_updated()  
  {  
    // no expect or verify calls needed, so you can keep this separate from the setup  
    m_facebook.AssertWasCalled(f => f.Update());  
  }
  
  [Test]  
  public void twitter_is_updated()  
  {  
    m_twitter.AssertWasCalled(t => t.Update());  
  }  
}
```

For simple mocking, you can use RhinoMocks' stub.AssertWasCalled() (confusing terminology) rather than .Expect(); this keeps things nicely separated and each test is tiny and only verifies the things it is interested in. If one of them fails, you still have the separation & readability.

The downside is that you have to go through the setup phase to follow the test and the test fixture is slightly less cohesive (as fields are set that aren’t used in every single test), but it's not too bad and I feel it's a sensible tradeoff.

I don't use this format as my default style, but it does come in handy for this type of situation. The main thing I take from this is it's horses for courses. There is no de-facto way to lay out your tests. Sometimes I use standard AAA, other times I use data driven, other times I use fixture-as-context.