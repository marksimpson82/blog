+++
title = "The fundamentals of unit testing: Tests shouldn't ape the production code"
tags = ["fundamentals of unit testing", "testing", "tips"]
path = "/blog/2012/11/12/the-fundamentals-of-automated-testing-tests-shouldnt-ape-the-production-code.html"
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

Aping the logic of the class under test is an bad idea when writing tests, but it's an easy mistake to make. 

## Aping... Bueller?

"Aping" simply means imitating/repeating the logic used in the class under test. In its simplest form, the problem can be illustrated like so: 

Production code:

```cs
public class Calculator  
{  
 public int Add(int a, int b)  
 {  
 return a + b; // actual logic of the class under test  
 }  
}
```

A test for the above class:

```cs
[Test]  
public void adding_two_numbers_returns_the_sum()  
{  
 // Arrange  
 var calculator = CreateCalculator();

 // Act  
 int result = calculator.Add(1, 2);

 // Assert  
 Assert.That(result, Is.EqualTo(1 + 2)); // ape alert, ooh ooh ooh! >:O  
}
```

Although this doesn't look like the end of the world, we can see that the test method line "Assert.That(result, Is.EqualTo(**1 + 2**))" is directly replicating the logic in the Add method. This is "aping".

## Why is this a bad thing?

This is bad for a few reasons. Firstly, if the class under test is bugged and the test apes its logic to get an expected answer, we've just reproduced the bug in our test code and erroneously passed the test. So, instead of having working production code, we have two bits of bugged code and a false sense of security.

Secondly, when writing tests, if state can be tested, it should be done using as declarative a style as possible - we don't want to say **how** we get to the answer, just **what** it should be. 

I don't want to see the test code literally add 1 and 2 to get 3. Instead, I want to see 3 in the test. Here's a fixed-up version of the test that does not ape the production code:

```cs
[Test]  
public void adding_two_numbers_returns_the_sum()  
{  
 // Arrange  
 var calculator = CreateCalculator();

 // Act  
 int result = calculator.Add(1, 2);

 // Assert  
 Assert.That(result, Is.EqualTo(3));  
}
```

You should always scan your test code looking for this anti-pattern. The example I've cited is very simple, but I've seen a lot of real world code that has succumbed to aping the production code resulting in bugs going undiscovered. 

## Validating your answers

You may be thinking, "OK genius, so you skipped adding 1 and 2 in the test code, but you must've known to follow the addition algorithm in your head to be able to come up with the answer of 3. How do you know your brain didn't get it wrong and the test is bugged?" 

It's a good question and the truth is, it's often the case that it's not clear-cut. However, there are steps you can take to validate your answers (or at least be a little more sure of them).

* Don't just assume you've got it right first time. Double check it for a few minutes more. 
* Write out some notes on paper (I sometimes do the testing version of truth tables). 
* Maybe you have a specification for this particular part. Use it to check the answer (stop laughing at the back, there! – it occasionally does happen; e.g. conventions for a maths library). 
* Use an alternative method to come up with the same answer (it's often the case that the same value can be calculated via multiple algorithms / schemes). 
* Use an existing implementation to corroborate your findings. E.g. if you're writing a test to make sure that JSON is validated correctly, then check that [JSONLint.com](http://jsonlint.com/) agrees with your test results. 
* If you're not sure how to corroborate an exact answer, then check any invariants you're aware of as a smoke test. If any of the invariants don't hold, your answer is probably wrong.