+++
title = "The pride of a programmer"
tags = ["testing"]
+++
I was thinking about this the other day, and something struck me (and no, it wasn't a disgruntled developer). Automated testing is a valuable and widely accepted part of the software engineering process. Many companies and organisations require that functionality be well tested prior to it being checked in and integrated into the main version control branch. As a result, developers can spend hour upon hour every week writing unit tests. In many cases, the quantity of test code can be more than double the code being tested!

If you give any programmer a problem to solve, their brains will start whirring and they will come up with numerous solutions. They will draw upon past experiences, new technologies and articles/books they've read. They will use specific parts of the language to elegantly solve the problem in a terse and expressive fashion. When they come up with a really cool solution, others will marvel at it and learn from it.

In short, most programmers will think critically about problems before, during and after solving them.

### The indifference of a unit tester

So, why is it that some folk just **stop thinking** when they put on their unit testing hat? I fully understand that testing is not as glamorous or fun as banging out production code, but that's no reason to accept sub-par test code.

Given that unit testing is part of the software development cycle, I personally think that anyone who [phones in](http://www.urbandictionary.com/define.php?term=phoned+it+in) their test code **is doing themselves a disservice**. If you do the minimum possible amount of work, do not think critically about what you're doing and ultimately learn nothing from it, then that's a lot of time that is thrown away every week.

It also doesn't say much about you as a developer if you phone it in. "Pff, functioning software, who needs that?"

Test code is still code. You have to write a lot of it. It is fundamentally entwined with the production code in that it is vital to proving the solution works. Moreover, if you test in a brain-dead fashion and fail to draw upon any of the faculties used when writing production code, you are often **making more work for yourself** later on, too. I usually cringe at the phrase _"work smarter, not harder_", but in this case it is often applicable.

### Testing informs design

Firstly, the most obvious point is that, if it's hard to test something due to it being at the mercy of the environment, static/global state, hard wired dependencies and such, then it's probably a sign that your code needs refactored. If you want to test a loop exit condition and end up having to connect to a real database to do so, you know you've got problems.

If you simply shrug your shoulders and plough on, you'll probably run into all kinds of obstacles. For example, you may have to initialise the environment to be **just right** for your test, then carefully negate the results of the test in the teardown. But then what if the test order matters? How will you know? I've been in this situation before and it's not pleasant. It was such a battle getting the environment configured correctly for each test that I lost the will to live. Plus the tests ran incredibly slowly.

One of the major benefits of unit testing is that it encourage you to split up functionality into discrete units. It just so happens that the discrete units are more easily understood as a result. I liken it to building blocks. Instead of having a monolithic structure (or, as less kind folk would call it, a [big ball of mud](http://en.wikipedia.org/wiki/Big_ball_of_mud)), you have a load of little blocks. Not only are the blocks much easier to understand on their own, but they are much nicer to work with. I won't bang on about this much because it's nothing new (see [Test Driven Development](http://en.wikipedia.org/wiki/Test_driven_development)).

I don't always practice TDD, but at the very least I try to test classes/methods not long after I've written them. Putting it off any longer tends to result in having to write a lot of test code at once, which sucks. If you don't like writing test code and you save up the tests for later, it's like putting off doing your school homework. It hangs over you like a cloud... and then you have to do it all at once on a Sunday night. Why punish yourself? :)

### Unit testing is programming, too

Naively attacking a testing problem may result in generating reams of test code that proves very little or, worse, has negative value.

When writing tests, I am constantly looking for the following warning signs:

  * You have to configure the environment / concrete collaborators in a fashion that you barely understand yourself (how is anyone else meant to deal with this?)
  * You can't easily test certain conditions or logical branches due to tight coupling (e.g. trying to test the behaviour of a class when one of its collaborators throws an exception that could occur in production systems, such as a network connection exception)
  * The test code is disproportionately large compared to the class under test due to repetition. The [DRY](http://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principle isn't just for production code (though tests should favour readability if push comes to shove).
  * The test code is convoluted. It is not clear what is going on, the test names are poor and it doesn't help you understand the class under test.
  * The tests are brittle, causing them to frequently break, and break badly (e.g. a change in a concrete collaborator breaks tests that shouldn't really depend on it, resulting in a debugging session rather than a simple fix...)
  * The test code could be refactored to use patterns to cut down on the noise (see previous Test Data Builder post).
  * The tests do not seem to prove anything. If a test calls some methods with trivial cases and does very little verification, then what's the point in writing the test?

If I encounter one or more of these signs, I try to think about whether the class under test or the _tests themselves_ would benefit from refactoring.

### Pointless Tests

The last point is in the list particularly salient. **Why write a test if it doesn't prove anything?** I find this to be the most insidious problem of all.

In general development, no self respecting programmer would repeatedly write code that:

  * Has no purpose
  * Looks like it's doing the job correctly, but actually isn't
  * Sets a bad example to anyone else reading the code
  * Sets good practices to one side (e.g. loads of repetition, unrepresentative method names)

Programmers should hold themselves to the same standards when writing tests. Bad testing is arguably worse than no testing at all.

Here's an example of a pointless test:

```cs
[Test]
public void SaveGameTest()
{
  var game = new Game();
  var serializer = new GamePersistence();

  using(Stream stream = new MemoryStream())
  {
    serializer.Save(game, stream);
  }

  Assert.IsTrue(true);
}
```

What does this prove? Nothing. At the very most, it proves that you won't encounter an exception when saving a game in the most trivial of cases.

What does it do that is harmful? Lots. It took time to write. It takes up space in the solution explorer / code file. It gives impression that functionality has been tested in some capacity. It skirts over areas of concern. It sets a bad example to other developers who may look to existing tests for an example of testing this sort of thing.

Finally, anyone who writes test code like this will probably find that it **makes them hate testing even more than before**, because they got absolutely **nothing** out of it. Bad tests rarely find any bugs because they're not asking the right questions, or any questions at all. If no bugs are found, then the testing pass feels like a waste of time, further reinforcing the dislike for testing.

### In Summary

Testing is part of the software development process. It has its own language, methodologies, patterns, best practices etc.

If you apply the same critical thought processes and rigour to testing that you apply to production code, you will write better software with fewer bugs. If you phone it in, you'll receive a return call down the line...