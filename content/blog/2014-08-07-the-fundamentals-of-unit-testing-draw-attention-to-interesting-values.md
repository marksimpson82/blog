+++
title = "The fundamentals of unit testing: draw attention to 'interesting' values"
tags = ["fundamentals of unit testing", "testing", "tips"]
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

3 is the magic number? No. No, it's not. 

Magic numbers/strings/other values in all walks of programming are a readability and maintenance liability. It's quite common to see all kinds of literals being littered through test code. It's quite easy to simply switch off and treat test code as a second class citizen.

To illustrate this point, please tell me what this does

```cs
[Test]  
public void TestInvalidFuelAmount()  
{  
 // Arrange  
 var car = CreateLittleCar(); 

 // Act & Assert  
 var exception = Assert.Throws<ArgumentException>(
   () => car.AddFuel(500));  
}
```

It's not exactly crystal clear, is it? Although the naming of this test can and should be improved, bear in mind that it's an extremely simple case (one method call with one argument being passed). Despite this, the intent is still obscured because of a literal.

<a name="Replace_magic_values_with_named_consts"></a> 

## Replace literals with named consts 

Let's change 500 to a named constant. Let's also change the test name while we're at it.

```cs
[Test]  
public void when_the_car_fuel_tank_capacity_is_too_low_and_fuel_is_added_an_exception_is_thrown()  
{  
 // Arrange  
 var car = CreateLittleCar();  
 const int LitresOfFuelThatIsTooLargeForTankCapacity = 500; 

 // Act & Assert  
 var exception = Assert.Throws<ArgumentException>(() =>  
 car.AddFuel(LitresOfFuelThatIsTooMuchForTankCapacity));  
}
```

Now that's much clearer. We can see what the value represents, the units it's measured in and its place in the test. Some people shit the bed when they see really long story-like variable names in tests, but they're generally a help, not a hindrance.

While the previous example is simple, this tip makes much more of a difference in situations where a function/method/constructor has numerous parameters, but the test is largely focused on only one of them. How do you know which one to pay attention to?

```cs
[Test]  
public void when_account_balance_is_low_money_transfers_fail_when_would_be_overdrawn()  
{  
 // Arrange  
 var currentAccount = GetCurrentAccountWithBalanceInUSD(10); 

 // Act  
 bool transferSucceeded = 
   currentAccount.TryTransfer(1000, 42, 602402); 

 // Assert  
 Assert.That(transferSucceeded, Is.False);  
}
```

Fine, this is a crufty-looking API, but in certain circumstances, it's quite common to see functions/constructors that take multiple arguments of a similar type. At a glance, how can you tell which of the arguments is the one of interest to the test? Is it 1000, 42 or 602402? What is the significance of any of them? Which one is causing the transfer to fail?

Let's use a named const to draw attention to the interesting argument.

```cs
[Test]  
public void when_account_balance_is_low_money_transfers_fail_when_would_be_overdrawn()  
{  
 // Arrange  
 var currentAccount = GetCurrentAccountWithBalanceInUSD(10);  
 const int AmountInUSDThatWillForceAccountIntoOverdraft = 1000; 

 // Act  
 bool transferSucceeded = currentAccount.TryTransfer(
   AmountInUSDThatWillForceAccountIntoOverdraft , 42, 602402); 

 // Assert  
 Assert.That(transferSucceeded, Is.False);  
}
```

Turns out the 42 is the number of cents in the transfer, and that 602402 is just a dummy customer number we're passing through. 

We can go further than this to clean things up still further by doing things such as:

* Extract a wrapper test method that calls TryTransfer, but only has one parameter: the amount of USD to withdraw (the other parameters can be satisfied with constants). This draws attention to the important part of the test (varying the value of the USD transfer amount) and also helps insulate the tests from changes to the TryTransfer method. 
* In the production code, using types that are more appropriate to reduce ambiguity (e.g. in the case of a customer account number, an AccountCredentials class would be more suitable than an int!) 
* Finally, if lots of things are changed in the tests, but in slightly different ways each time, consider the use of a [Test Data Builder](@/blog/2009-04-10-the-test-data-builder-pattern-with-c-30.md). Test data builders are very useful, as the provided defaults are sensible for most cases. As a result, when arranging your test, the only things that are changed in the builder are the things that actually matter. Test data builders can also insulate the tests from breaking changes.