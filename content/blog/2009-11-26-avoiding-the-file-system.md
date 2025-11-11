---
id: 438
title: Avoiding the file system
date: 2009-11-26T20:21:31+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=438
#permalink: /?p=438
tags:
  - 'c#'
  - patterns
  - testing
---
Going from experience and, as illustrated by Misko's recent presentation, the more dependencies you have on your environment, the less trustworthy and maintainable your tests become. One of the foremost offenders in this area is touching the file system.

Any time someone says "hey, I'm trying to open a file in a unit test...", my first reaction is to say "woah", and not in the "I know Kung Fu" way! If you introduce a dependency on the file system, bad things are more likely to happen. You now depend on something that may not be there/accessible/consistent etc. Ever written a test that tried to access a common file, or read a file that something else may write to? It's horrible.

It is for these reasons that many folk will say "it's not a unit test if it hits the file system". In particular, if you have a TestFixtureSetUp/TearDown method that deletes a file, it's a sure sign that the fixture is going to flake out at some point.

### A real example

Recently at work, my colleagues have experienced the joy of a **huge** refactoring job pertaining to restructuring our projects/solutions to reduce build times and increase productivity. This work included maintaining something close to ten thousand tests.

As the job progressed, they kept finding that some test fixtures did not live in isolation. The tests depended on various things they shouldn't have and, most saliently, file dependencies proved to be a total pain in the balls. Everything built OK, but when run, the tests failed due to missing files. Paths and file attributes had to be checked (Copy if newer, etc.), lost files had to be hunted down and so forth. It's hassle that people don't need! As I've stated before, when it comes to testing, maintenance is king.

Anyway, if you have a hard dependency on the file system, consider the alternatives. This is never a **hard** rule as it is not suitable for all uses, but it always worth thinking about.

### Alternative approaches

Firstly, [abstract the file operations to](http://stackoverflow.com/questions/1528134/unit-testing-file-i-o/1528243#1528243) some degree. You can do numerous things here, from changing the internal loading strategy (via [Dependency Injection](http://en.wikipedia.org/wiki/Dependency_injection)) to - even better - separating the loading/use of the file so that the consumer of the file's contents **doesn't even have to care** about the loading strategy.

Once you've done this, you no longer need to use files in your unit tests, as you can use plain ol' strings, streams or even just directly construct instances to represent the contents of the file.

Say we had a simple class called "MyDocument", and MyDocument could be loaded from a .doc file on disk. The simplest approach would be to do something like this:

#### Approach One

```cs
// #1: this is tightly coupled to file system. 
void SimpleLoading()
{
  var simpleDocument = new MyDocument("filenameToLoad.doc");
}
```

Depending on your needs and the demands of the user, this may be OK. However, to test MyDocument's methods/properties properly, we need access to the file system to instantiate it. If our tests are to be robust & fast, we need something better. Here's something that's testable:

#### Approach Two

```cs
// #2: doc calls DocumentLoader's methods to get data needed
void SlightlyImprovedAndTestable()
{
  // this type implements IDocumentLoader
  var docLoaderStrategy = new FileDocumentLoader("filenameToLoad.doc");

  // Uses DI; ctor calls doc loader's methods to construct itself
  var doc = new MyDocumentType(docLoaderStrategy);
}
```

From a testability standpoint, this is slightly better, as we can now feed in an IDocumentLoader instance which the MyDocument constructor uses to get the data.

On the flipside, the MyDocument type now needs to know about IDocumentLoader. To load a document, the user now needs to know about creating an IDocumentLoader and feeding it into the constructor - it's more complicated. I often see people do this as the default step for abstracting their file operations - they alter the code to make it testable, but fail to spot the problems it brings if done at the wrong 'level'. If you gnash your teeth every time you have to use your own code, it's a warning sign that something is wrong.

When we think about it though, why should MyDocument need to know about loading strategies? In many cases, we can parse a file and produce some output using a factory or builder instead. E.g.:

#### Approach Three
```cs
// #3: Break loading + doc creation into two distinct parts
void DecoupledAndTestable()
{
  // loading is now a separate step :)
  MyDocument doc;
  using(var docLoader = new DocumentLoader("filenameToLoad.doc"))
  {
    doc = docLoader.LoadDocument();
  }

  // Similarly, we can do something like this
  var testDoc = new TestLoader()
    .LoadDocumentFromText(SomeResourceFile.ValidDocument);
}
```

To clarify how this works: The DocumentLoader would parse the .doc file and construct the object instances required to build up a real document, then pass them into the document's constructor (or build up the document via some other means, such as iteratively calling methods on a blank document to fill it up as new items are found - whatever makes sense). This totally decouples the loading and instantiation, meaning we can test each step in isolation.

I.e. the flow goes: Read Input => Parse Input => Create Document from Parsed Input

### Life after the File System

Once you're no longer dependent on the file system, you are free to use one of many strategies for loading/creating your type. Depending on the abstraction, some options include:

  * Just declare your data inline in the test methods as a const string, or as a const/readonly field of the test fixture. This works well for small amounts of text.

  * Add your test files as text file resources. You can then access the file contents as a static string property. This is handy, as you get a strongly typed resource name and don't need to mess around with paths + copying files. This works well for larger sets of data, or data you want to re-use in multiple tests.
  * Use embedded resources & [GetManifestResourceStream](http://msdn.microsoft.com/en-us/library/xc4235zt.aspx). This is slightly messier; it doesn't require copying files, but it does require that the namespace + filenames used to reference the embedded resources are correct (runtime failures ahoy). You also need to handle streams when using this method.

If my loading logic deals with strings, I tend to just build an 'inner' parser that works with the strings, then wrap it in another class that opens and reads files, then passes the (raw) string to the 'inner' parser class. This allows me to thoroughly test the parsing logic independent of the file system, but also means I can re-use it for test classes or other cases. I.e. I can exercise more of the production code without any of the file system pain :)

Depending on the thing being loaded, this isn't always the best solution, but for relatively simple loading I tend to favour this method.