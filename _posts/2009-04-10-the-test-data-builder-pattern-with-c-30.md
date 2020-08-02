---
id: 147
title: The Test Data Builder pattern with C# 3.0
date: 2009-04-10T00:53:14+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=147
#permalink: /?p=147
tags:
  - 'c#'
  - patterns
  - testing
---
**Update**

Since writing this, I&#8217;ve come to prefer the original  method chaining style.  While the property initialiser style works very well for simple builders, the original method chaining style works a bit better if you have nested builders.  See the link in this post for the original; it&#8217;s more versatile.

### The problem

If you write automated tests, then you are bound to have come across a situation where, during the course of testing your classes, you have to configure them in different ways.  This difference may be slight (say, varying one argument passed into a constructor every time), but it is enough to make instantiating the objects a pain.  You can&#8217;t use a common setup method to make life easier, so that leaves you with two obvious options:

  1. Instantiate the objects via a direct constructor call
  2. Abstract the creation a little and use multiple factory methods

### Drawbacks

The first option is verbose, cumbersome and brittle.  Every time the constructor changes or its rules change (e.g. &#8220;parameter string houseName must not contain spaces&#8221;), you&#8217;ll need to update the tests to use the new form.  If you have scores of calls, writing and maintaining the tests can consume a lot of time, plus it&#8217;s tedious.

The second option may seem appealing, but it also has shortcomings.  This is the so called &#8220;Object Mother&#8221; pattern.  You basically have some factory methods (or a test class) that returns objects in various configurations.  When you have method names like &#8220;CreateHouseWithKitchenSinkAndStairs&#8221;, &#8220;CreateHouseWIthKitchenSinkAndRoof&#8221; and &#8220;Create HouseWithRoof&#8221; (or equivalent overloaded methods) then you&#8217;ll recognise this.

Depending on how much method re-use you can share between tests, this may also be brittle and a lot of effort to maintain.  Both ways of doing things also lack clarity when lots of arguments are being passed around &#8212; the intent of the test (read: the _interesting_ argument[s]) can be hidden by the noise of setting up safe defaults.  E.g. If you have 10 &#8216;normal&#8217; objects and one badly formatted string that you&#8217;re using to make sure that an exception occurs, you want to focus on the argument that will cause the exception, not other parts.

### Test Data Builders

So&#8230; what is this mythical Test Data Builder pattern?  It&#8217;s actually quite simple, though the syntax can look strange if you haven&#8217;t come across fluent interfaces before.

A Test Data Builder is an extension of a standard factory method.  The difference between a standard factory and a builder is the way that the builder wires things up.  A factory typically has a &#8220;Create&#8221; call which creates an instance of an object (or objects) in pre-defined configurations, or with some customisability provided via arguments in the Create call, or injected into the factory&#8217;s constructor.

A TDB varies this approach by setting up default, safe values to be used to instantiate the class under test.  When the builder&#8217;s constructor runs, it creates these defaults and stores them as fields.  There is usually a one to one correspondence of the class under test&#8217;s parameter list and the values stored in the builder.

The cool part is that anyone using the TDB can selectively modify these values by calling methods or setting properties on the TDB.  Finally, when the TDB has been configured satisfactorily for the test, its Build method is called, injecting its fields into the class under test&#8217;s constructor as arguments.

Nat Pryce posted [an excellent article on Test Data Builders](http://www.natpryce.com/articles/000714.html) so I would implore you to read it before reading the rest of this post.

### Terser is more gooder &#8211; C# 3.0

Once I&#8217;d got my head around the strange fluent interface syntax, I found that example to be invaluable.  It got me thinking: what if we could write these builders in an even more concise fashion?  Well, we can.  C# 3.0 can go one step further and, through the use of object initialisers, eliminate the need for method chaining.  This results in terser syntax still.

It&#8217;s simple: Instead of using a method per value change, we use a property instead.  Since object initialisers are run immediately after a constructor and are nicely grouped, it means we can create and configure our builder in one step.

The following code is provided merely to illustrate the syntax (there&#8217;s not much point in using a TDB on a class with so few parameters).  Here&#8217;s an overly simple example of a Person class to test.

<pre>    /// &lt;summary&gt;The class under test&lt;/summary&gt;
    public class Person
    {
        private readonly string     m_name;
        private readonly DateTime   m_dateOfBirth;
        private readonly string     m_address;

        public Person(string _name, DateTime _dateOfBirth, string _address)
        {
            ValidateDateOfBirth(_dateOfBirth);
            ValidatePostCode(_address);        // etc.
            m_name          = _name;
            m_dateOfBirth   = _dateOfBirth;
            m_address       = _address;
        }
    }</pre>

Here&#8217;s the builder.  Notice that it has 3 auto properties that match the Person class&#8217;s constructor parameter names and types.  Default values are instantiated in the constructor, and the properties allow test writers to swap out the defaults for their own specific values.

<pre>    /// &lt;summary&gt;Test data builder for testing the Person class&lt;/summary&gt;
    public class PersonTestBuilder
    {
        public string   Name        { get; set; }
        public DateTime DateOfBirth { get; set; }
        public string   Address     { get; set; }

        public PersonTestBuilder()
        {
            Name        = "DefaultName";
            Address     = "DefaultAddress";
            DateOfBirth = new DateTime(1920, 8, 15);
        }

        public Person Build()
        {
            return new Person(Name, Address, DateOfBirth);
        }
    }</pre>

Finally, here&#8217;s the test code itself.  Notice that the only arguments that are varied are the ones that are named in the test.  If the builder&#8217;s property is not set, the defaults held in the builder are used to construct the instance of the class under test.

<pre>    /// &lt;summary&gt;The actual tests for the person class&lt;/summary&gt;
    [TestFixture]
    public class PersonTests
    {
        [Test]
        [ExpectedException(typeof(RidiculousAgeException), ExpectedMessage = "... etc")]
        public void Constructor_DateOfBirthInvalid_ThrowsExceptionTest()
        {
            new PersonTestBuilder
                {
                    // Notice that this is now the sole focus!
                    DateOfBirth = new DateTime(1200, 10, 15)
                }.Build();
        }

        [Test]
        public void Constructor_AddressTest()
        {
            Person testPerson = new PersonTestBuilder
            {
                Address = "10 Bigglesworth Lane",
            }.Build();

            Assert.That(testPerson.Address,
                Is.EqualTo("10 Bigglesworth Lane"));
        }
    }</pre>

If any of this is unclear, just paste the code into your IDE and step through it in your debugger to see what&#8217;s happening (you&#8217;ll have to remove the non existent methods & exception test, obviously!)

### Summary

I&#8217;ve found the following advantages when using this pattern in tests with large amounts of setup and little commonality in object construction:

  1. Less fragile.  Since object creation is centralised and uses safe values by default, tests are more resistant to change compared to direct constructor calls.
  2. Terser test code (extremely important when setup is complicated)
  3. The intent of the test is clearer.  There is less noise in test code, so you can more easily pick out the arguments/interactions of interest.