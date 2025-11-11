---
title: "The fundamentals of unit testing: Data-driven tests"
date: 2020-08-05T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - fundamentals of unit testing
  - testing
  - tips
---

This post is [part of a series]({% post_url 2012-10-24-the-fundamentals-of-automated-testing-series %}) on unit testing.

## Don't Repeat Yourself (DRY) 
If you've been programming for more than a few years, you've mostly likely heard the phrase [**D**on't **R**epeat 
**Y**ourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) (DRY) and have applied it to your code. 

The main thrust of DRY is avoiding duplication across code, data, abstractions etc. The benefits include increased code 
clarity, brevity and the creation of a single source of truth (it should be noted that blindly applying the DRY 
principle can be harmful, but that's for another day).

## DRY fail in test code
So, that's DRY in production code. Seems straightforward. 

If you've been writing automated tests for a while, you've also probably noticed that it's very easy to repeat ourselves 
when writing tests, particularly when we wish to vary the test data while retaining the same test logic. 

### A simple example
Let's take a very simple example: We're going to test the `Python` addition operator:

```python
class AdditionOperatorTests(TestCase):    
  def test_add_a(self):
    self.assertEqual(2 + 2, 4)
 
  def test_add_b(self):
    self.assertEqual(2 + 3, 5)

  def test_add_c(self):
    self.assertEqual(3 + 10, 13)
```

#### Problems with this approach
If you look at this python example, we can say a few things:
1. The test names aren't particularly descriptive -- it feels like we're fighting to come up with a useful name, but 
can't.

1. The test _logic_ (the assert in this case) is identical across all three tests -- we've violated the DRY principle.

1. The bulk of the test lines are boilerplate/noise. All we're really interested in is varying the data here. 

For more complicated test cases (especially those that have more intricate 
[Arrange, Act & Assert]({% post_url 2014-08-07-the-fundamentals-of-unit-testing-arrange-act-assert %})) logic, the
duplication soon gets out of control. 

### A solution: data-driven testing
Data-driven testing is much what it sounds like -- the test logic is written once, and we data-drive the test by 
passing in multiple values.

Most languages have testing frameworks that support data-driven testing. For example, Python has the 
[ddt](https://ddt.readthedocs.io/en/latest/example.html) package. Installing it is as simple as `pip install ddt`. 

We can now re-write our addition operator tests to use a single method and multiple test data inputs:

```python
from unittest import TestCase
from ddt import ddt, data, unpack

@ddt
class AdditionOperatorTests(TestCase):
  @data(
    (2, 2, 4), 
    (2, 3, 5), 
    (3, 10, 13))
  @unpack
  def test_add(self, a, b, expected):
    self.assertEqual(a + b, expected)
``` 

It works via three special decorators:
* `@ddt`: marks the TestCase-derived class as being data-driven.
* `@data`: contains the test data values.
* `@unpack`: (optional) automatically unpacks the `@data` contents `=>` method args (if you omit this, your test will 
receive a single argument and you must unpack the contents yourself).

#### Wrapping up
Let's revisit the three problems we previously talked about:

1. The awkward naming problem has disappeared. 

1. The test _logic_ is defined once. It's DRY.

1. Even in this artificially simple example, the number of lines in the test scales with the amount of test _data_. 
If we want to add another test, we probably just need to add a single line. 
