---
id: 660
title: Data-Driven Testing with Python
date: 2012-05-21T22:29:05+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=660
#permalink: /?p=660
tags:
  - data-driven
  - python
  - software
  - testing
  - tips  
---
Hello tests. It’s been a while since I blogged about automated testing, so it’s nice to welcome an old friend back to the fold. I’ve missed you. I’ve recently started programming in python. I say programming, but what I mean by that is ‘hopelessly jabbing at the keyboard and gawping as my lovingly written code explodes on being invoked’. While I blub.

Python is a dynamic programming language. It’s pretty dynamic in its ability to detonate in various ways, too. There’s no compiler to sanity check my elementary mistakes like typos, or dotting onto a method that doesn’t exist. Or accidentally comparing functions instead of values. Or... well, you get the gist.

Anyzoom, the fundamentals of unit testing in python are very simple. I can’t be bothered detailing how to use unittest or a test runner, as there’s nine zillion resources out there on it already. 

# A Simple Setup
We’re using [unittest](http://docs.python.org/library/unittest.html) as the framework, [Nose](http://readthedocs.org/docs/nose/en/latest/) as the runner and [TeamCity Nose](http://pypi.python.org/pypi/teamcity-nose) integration. It worked very nicely out of the box, so I can’t complain. Writing tests is simple, but then I wanted to make a data-driven test and...

# Data Driven?
To recap what a data-driven test is: You run the same test logic and assertions, but vary the data. E.g. if you have a test method that is part of a test suite, you’d expected to see something like this (pseudo python code):

```python
test data = Vector3D(0,1,0), Vector3D(0,1,0), 1.0
test data = Vector3D(0,1,0), Vector3D(0,-1,0), -1.0
test data = Vector3D(0,1,0), Vector3D(1,0,0), 0.0

def test_dot(vec1, vec2, expected_result):
  dot = Vector3D.dot(vec1, vec2)
  assertEquals(dot, expected_result)
```

Each of the test data cases defined above the function / method would generate a new test case. The test logic would be run 3 times – one for each test input.

Data-driven tests typically take input data, feed it into some method or function, then assert that the produced effect is correct. You’ll often need to pass through an expected result, too.

# The Options

I had a quick scout around and arrived at two options. There is a third, but it has a limitation that I didn’t much care for.

## nose generators

It sounds like a high-tech energy solution based on harnessing snot. It’s not. 

Nose (the test runner we’re using) has a built-in concept of [test function as generators](http://readthedocs.org/docs/nose/en/latest/writing_tests.html#test-generators). This allows users to create multiple test cases out of single tests. At first glance, it looks good. Unfortunately, [as detailed here](http://technomilk.wordpress.com/2012/02/12/multiplying-python-unit-test-cases-with-different-sets-of-data/), it doesn’t work when you’re subclassing unittest.TestSuite which is a common thing to do. 

If you don’t care about this limitation _and_ use Nose to run your tests, I actually think this is a nice solution.

## ddt

Next up is a one called simply, “[ddt](http://technomilk.wordpress.com/2012/02/12/multiplying-python-unit-test-cases-with-different-sets-of-data/)”. No prizes for guessing what that acronym stands for (no, really, there is no prize. Stop phoning. This is a repeat, the lines have closed).

To use ddt, decorate your class with @ddt, then add @data to data-driven test methods. Each argument specified as part of the @data decorator generates a test case, so if you have N arguments, you get N test cases.

The examples don’t make it crystal clear, but with ddt, you’re expected to boil down your test case to this single argument. I.e. if you have a few inputs and an expected result, you’re responsible for stashing the data into a containing object and yanking it back out in the test method.

I’m not a massive fan of this approach as I’m quite accustomed to the NUnit style of the test runner reflecting over my test data attribute arguments then [passing the correct arguments to my test method automatically](http://www.nunit.org/index.php?p=testCase&r=2.5). However, it gets the job done and works well enough. 

Possibly due to being ill at ease with Python, I made a wrapper object to avoid having to use a dictionary. Personally, I think this makes the test code read better, but this is just a matter of taste.

Note: This bit of code may make a pythonista strangle you with your own tie (I don’t wear one).

```python
class TestData:
  def __init__(self, **entries):
    self.__dict__.update(entries)
```

It’s then just a case of instantiating a new TestData object every time you want to pass several arguments into a test method, like so:

```python
@data(
  TestData(vec1=Vector3D(0,1,0), vec2=Vector3D(0,1,0), expected_result = 1.0),
  TestData(vec1=Vector3D(0,1,0), vec2=Vector3D(0,-1,0), expected_result = -1.0),
  TestData(vec1=Vector3D(0,1,0), vec2=Vector3D(1,0,0), expected_result = 0.0)
)
  def test_dot(self, test_data):
    vec1 = test_data.vec1
    vec2 = test_data.vec2
    dot = Vector3D.dot(vec1, vec2)
    self.failUnlessAlmostEqual(dot, test_data.expected_result, places=1)
```

**Updated March 2014:** The developers of ddt were nice enough to add an @unpack decorator! You can now provide lists/tuples/dictionaries and, via the magic of @unpack, the list will be split into method arguments.

Documentation is here: [http://ddt.readthedocs.org/en/latest/example.html](http://ddt.readthedocs.org/en/latest/example.html "http://ddt.readthedocs.org/en/latest/example.html")

## nose-parameterized

The final option I was made aware of (thanks to my old colleague Gary) is one called [nose-parameterized](https://github.com/wolever/nose-parameterized). As you can imagine, it works with nose. It allows parameterised tests. What’s not to like?

Well, the truth is... This one is almost perfect. Usage (from the documentation):

```python
@parameterized([
  (2, 2, 4),
  (2, 3, 8),
  (1, 9, 1),
  (0, 9, 0),
])
def test_pow(base, exponent, expected):
  assert_equal(math.pow(base, exponent), expected)
```
Each tuple’s contents is expanded into the test method’s parameter list, just like momma used to make. Beautiful!

... so why am I using ddt instead? Unfortunately, nose-parameterized does not play nicely with PyCharm. PyCharm lets you run the tests from the IDE and also debug them, but nose-parameterised seems to confuse it.

Gary said, “what are you doing man, using an IDE with Python?” The truth is that I’m not a real man. Yet.

# Roundup

In all honesty, all three options are viable and it’s mostly down to preference. So there we go: Three good options for data-driven testing. If you have any other good ones, please leave a comment.

Happy testing!