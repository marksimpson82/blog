+++
title = "The fundamentals of unit testing: Setup structure"
tags = ["fundamentals of unit testing", "testing", "tips"]
path = "/blog/2020/08/10/the-fundamentals-of-automated-testing-setup-structure.html"
+++

This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

## The importance of test setup structure 
I've already blogged about the importance of well-structured test setup code in this series (have a look at
[Arrange, Act & Assert](@/blog/2014-08-07-the-fundamentals-of-unit-testing-arrange-act-assert.md) and 
[Use Factories](@/blog/2012-11-11-the-fundamentals-of-automated-testing-use-factories.md)). However, I've yet to 
touch upon the pros & cons of using the built-in framework `setup` & `teardown` methods.

### Setup & teardown methods?
If you've used well-known testing frameworks, you'll likely be familiar with some variant of these. They're optional 
methods that the framework runs for you automatically before each test is executed (`setup`) and after each test is 
executed (`teardown`).

Here's a few example links:
- Python: [`unittest`](https://docs.python.org/3/library/unittest.html) -- 
([setup](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp) / 
[teardown](https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDown))
- C#: [`NUnit`](https://docs.nunit.org/) -- 
([SetUp / TearDown](https://docs.nunit.org/articles/nunit/writing-tests/setup-teardown/index.html))
- C++: [`googletest`](https://chromium.googlesource.com/external/github.com/google/googletest/+/HEAD/googletest/docs/) 
-- ([SetUp / TearDown](https://chromium.googlesource.com/external/github.com/google/googletest/+/HEAD/googletest/docs/faq.md#ctorvssetup))

**Aside**: It should be noted that many test frameworks define additional methods that might execute when a 
test `fixture` (or `class`) is created/destroyed, but we'll just focus on `setup` & `teardown` for now.

### Batteries included?
Because these conventional methods are included in the framework, they often become our default way of doing things. 

However, I've never much cared for using them and I'll do my best to explain why.

## A contrived example
Before I get going, here's some example C# test code that uses NUnit's `SetUp` and `TearDown` methods. We use NUnit's 
`SetUp` method to initialise the `BankAccount` with no funds available. The tests then make use of the 
already-initialised `BankAccount` instance to test functionality related to depositing funds.

There's also some iffy-looking static state relating to `AuthenticationService`, and we're leaning on the `SetUp` &
`TearDown` methods to make sure the instance is in a good state.
 
```cs
class BankAccountTests 
{
  static AuthenticationService ms_authService = 
    new AuthenticationService();
  BankAccount m_account;

  [SetUp]
  public void Init()
  {
    const decimal InitialBalance = 0.0m;
    m_account = new BankAccount(InitialBalance);

    // let's imagine the account must be marked as accepting deposits
    // before we can proceed due to some security features
    m_account.AcceptDeposits();  
    ms_authService.Begin();
  }
  
  [TearDown]
  public void Cleanup()
  {
    ms_authService.End();
  }

  [Test]
  public void DepositingFundsIncreasesAccountBalance()
  {
    m_account.DepositFunds(1000.0m, Currency.USD);
    
    Assert.That(m_account.FundsAvailable, Is.EqualTo(1000.0m));
  }

  [Test]
  public void WithdrawingFundsThrowsWhenAccountBalanceIsZero()
  {
    Assert.Throws<InsufficientFundsException>(
      () => m_account.WithdrawFunds(10.0m, Currency.USD));
  }
}  
```

There's multiple things I don't like about this.

### Problem: the code jumps around a lot. 
Because framework methods are 'automagic' (they're similar to
[Template Methods](http://wiki.c2.com/?TemplateMethodPattern), but are often called via reflection), the code no longer 
reads in a straight line -- it jumps around. 

Where do you naturally begin reading the code? 

* Do you start from an individual test?
* Do you start from the arbitrarily named method that has the [`Setup`] attribute above it? 
* Hmm, what if the test fixture also uses a 
[[`OneTimeSetup`]](https://docs.nunit.org/articles/nunit/writing-tests/attributes/onetimesetup.html) method, too? 
* What if the fixture is derived from a base fixture that has some (or all) of these methods?

It quickly becomes the testing equivalent of voodoo, and the only way to be 100% sure is to step through the code in a 
debugger. This is **not** what we want in test code. While test code can be verbose at times, it should be as simple as 
possible.

If you need to share code, follow the same practices as when writing production code. [Prefer composition over 
inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance) unless there's a strong reason to do otherwise.

### Problem: setup/teardown code quickly becomes misleading
Adding new tests to an existing fixture is an everyday occurrence. 

One day we decide to cover off a potential edge-case by adding a test that ensures a `BankAccount` with a positive 
balance will correctly receive a deposit. Easy, right? We add the following test:  

```cs
[Test]
public void DepositingFundsWhenAccountBalanceIsAboveZeroIncreasesBalance()
{
  // Arrange
  const int InitialBalance = 1000.0m;
  m_account = new BankAccount(InitialBalance);

  // Act
  m_account.DepositFunds(1000.0m, Currency.USD);
    
  // Assert
  Assert.That(m_account.FundsAvailable, Is.EqualTo(2000.0m));
}
```

There's a wrinkle, though: we realise that the `[Setup]` method has already created a `BankAccount` with a balance of 
zero, and the `[SetUp]` method _always_ runs. That's no good for our test case, though. We work around it by simply 
re-creating the `BankAccount`. Unfortunately, we forgot to call `AcceptDeposits()`, so the test fails.

Even in a simple example, the moment the `setup` code ceases to apply to _all_ cases in the test fixture, things start 
to get... muddy. 

At best, you'll apply _some_ setup logic in your `setup` method only to finish it off in your specific test methods. 
This is a type of two-phase initialisation. It's confusing, especially when the initialisation code jumps around. 

At worst, you'll do misleading work in `setup` only to throw it away, or even introduce bugs in the test code. This 
wastes time and will confuse your fellow programmers.

Another equally questionable solution is to split the fixture in two. We then group the sets of tests into the 
appropriate fixture depending on their `setup` needs. This is very inflexible form of coupling.
  
### Problem: setup/teardown code can hide bad habits
In the example above, we're able to work-around the problems caused by static state by performing bookkeeping in our
`setup` & `teardown` methods. 

It's also quite common to see developers use `setup` & `teardown` methods to skirt around the fact that they're 
[hitting the file system](@/blog/2012-11-02-the-fundamentals-of-automated-testing-atomic.md) in a unit test (at 
which point it's not really a unit test: it'll run slower & be more prone to breakages). 

Tests are consumers of your API, and if you're having to perform awkward state management via the use of `setup` & 
`teardown` to keep things rolling, it's often a sign that the class under test is not terribly easy to use.

### Solutions
1. [Use Factories](@/blog/2012-11-11-the-fundamentals-of-automated-testing-use-factories.md)
1. [Object Mother](http://wiki.c2.com/?ObjectMother) (read the caveats, though)
1. [Test Data Builders](http://www.natpryce.com/articles/000714.html)

Each of these alternatives is relatively simple, can be called directly by a test method and offers some level of 
configurability. Factory methods are the easiest to get going with. 

Want a `BankAccount` pre-configured with a set balance? No problem! Simply add a method that initialises and returns 
one. Every test is responsible for its own setup. Tests are no longer coupled to a one-size-fits-all `setup` method.

Object Mothers & Test Data Builders require a bit more up-front investment, but they pay it back in spades via providing 
canned objects with sensible defaults in a variety configurations. 

Let's re-write our example tests to incorporate some of these things:

```cs
class BankAccountTests 
{
  private BankAccount CreateBankAccount(
    decimal openingBalance=0.0m)
  { 
    // we've refactored the production code to get rid of the 
    // static dependency, so AuthenticationService has gone. 
    var account = new BankAccount(openingBalance);
    account.AcceptDeposits();
    return account
  }  
  
  [Test]
  public void DepositingFundsIncreasesAccountBalance()
  {
    var account = CreateBankAccount();
    account.DepositFunds(1000.0m, Currency.USD);
    
    Assert.That(account.FundsAvailable, Is.EqualTo(1000.0m));
  }

  [Test]
  public void WithdrawingFundsThrowsWhenAccountBalanceIsZero()
  {
    var account = CreateBankAccount();

    Assert.Throws<InsufficientFundsException>(
      () => account.WithdrawFunds(10.0m, Currency.USD));
  }

  [Test]
  public void 
    DepositingFundsWhenAccountBalanceIsAboveZeroIncreasesBalance()
  {
    // Arrange
    const int OpeningBalance = 1000.0m;
    var account = CreateBankAccount(OpeningBalance);

    // Act
    account.DepositFunds(1000.0m, Currency.USD);
    
    // Assert
    Assert.That(m_account.FundsAvailable, Is.EqualTo(2000.0m));
  }
}  
```

### Conclusion
I personally think the refactored test code is a lot easier to understand and extend.

- Each test reads linearly (no more ping-ponging around to understand the execution flow -- we're now dealing with a 
handful of simple factory methods).
- Each test can piggy-back on the default setup via a factory method, or have its own specific factory method.
- We're no longer using `setup`/`teardown` methods as a crutch for managing dodgy static dependencies.