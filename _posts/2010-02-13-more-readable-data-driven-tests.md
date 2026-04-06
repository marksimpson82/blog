---
id: 514
title: More readable data-driven tests
date: 2010-02-13T18:28:00+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=514
#permalink: /?p=514
tags:
  - 'c#'
  - testing
  - tips
  - data-driven
---
When the logic of a test method remains constant but the data varies, data-driven testing is a great tool. It allows you, the test author, to write compact code and to add new test cases rapidly. Unfortunately, data-driven tests have a disadvantage: The inputs are often less readable.

### A simple example
Let's take an example; testing Rob Conery's [PagedList implementation](https://blog.wekeroad.com/2007/12/10/aspnet-mvc-pagedlistt/). A page is basically a slice of the data returned by a linq query. If more data exists beyond the 'slice' represented by the PagedList<T> instance, its "HasNextPage" property should return true to indicate that it is available. Now, suppose we want to test whether a particular page has a next available page. Three things spring to mind that can influence the result: The page size, the current page index and the number of items in the list.

Here's a quick data-driven test for HasNextPage:

```c#
[TestFixture]
public class SimpleDataDrivenTest
{
  [TestCase(1, 1, 0)]
  [TestCase(1, 2, 0)]
  [TestCase(4, 2, 1)]
  [TestCase(10, 10, 0)] // etc
  public void HasNextPage_WhenNextPageDoesNotExist_ReturnsFalse(int itemCount, int pageSize, int pageIndex)
  {
    var pagedList = CreatePagedList(itemCount, pageSize, pageIndex);
    Assert.That(pagedList.HasNextPage, Is.False,
      "shouldn't be a next page, as there are not enough items");

}
  private IPagedList CreatePagedList(int itemCount, int pageSize, int pageIndex)
  {
  // imagine this creates a new instance of Pagedlist<T> with the above arguments as inputs
  throw new NotImplementedException();
  }
}
```

As you can see, the method itself is readable, but the parametrised values fed in via the [TestCase] attribute are not. It's really hard to keep everything in your head and remember what each number maps to in the function, especially when the method parameter types are all identical. If you have a list of 20 [TestCase] attributes, you start wondering what's for your tea and forget that the second value is the (checks image) page size. Mince. Mince for tea.

Hmm, if only we could those TestCases more readable; something like object initializers would be ideal.

### A simple trick: Subclass TestCase

My friend Hughel helped me come up with this one and it works quite well. Simply subclass the TestCaseAttribute class and add your own properties to represent the test parameters. It gets a little bit hairy when you have to access the Arguments array directly (especially since Attributes can be _weird_), but in practice, it works fine. In most of the tests, we're only interested in parametrising three things, so it's simple to add them as properties.

```c#
public class PageTestCaseAttribute : TestCaseAttribute
{
  public PageTestCaseAttribute() : base(0, 0, 0) {}
  public int ItemCount
  {
    get { return (int) Arguments[0]; }
    set { Arguments[0] = value; }
  }

  public int PageSize
  {
    get { return (int) Arguments[1]; }
    set { Arguments[1] = value; }
  }

  public int PageIndex
  {
    get { return (int) Arguments[2]; }
    set { Arguments[2] = value; }
  }
}
```

### The end result
Finally, we apply these attributes to our data-driven test, significantly improving the readability!

```c#
[TestFixture]
public class ReadableDataDrivenTests
{
  [PageTestCase(ItemCount = 1, PageSize = 1, PageIndex = 0)]
  [PageTestCase(ItemCount = 1, PageSize = 2, PageIndex = 0)]
  [PageTestCase(ItemCount = 4, PageSize = 2, PageIndex = 1)]
  [PageTestCase(ItemCount = 10, PageSize = 10, PageIndex = 0)]
  public void HasNextPage_WhenNextPageDoesNotExist_ReturnsFalse(
    int itemCount, int pageSize, int pageIndex)
    {
      var pagedList = CreatePageList(itemCount, pageSize, pageIndex);

      Assert.That(pagedList.HasNextPage, Is.False,
        "shouldn't be a next page, as there are not enough items");
    }
  )
}
```

I would hasten to add that I don't recommend using this approach willy-nilly - only when you have a large amount of tests that are parametrised by the same data types, causing the test cases to become hard to follow. I've used the `[TestCaseSource]` attribute and the `[TestCase]` attribute a lot in the past and most of the time it's not a problem.
