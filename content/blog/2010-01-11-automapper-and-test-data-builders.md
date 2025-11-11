+++
title = "AutoMapper and Test Data Builders"
tags = ["c#", "patterns", "testing", "tips", "automapper"]
+++
I've recently been tinkering with WCF and, as many people already know, writing data transfer objects is a pain in the balls. Nobody likes writing repetitive, duplicate and tedious code, so I was delighted when I read about [AutoMapper](http://www.codeplex.com/AutoMapper). It works really nicely; with convention over configuration, you can bang out the entity => data transfer code in no time, the conversions are less error prone, the tests stay in sync and you're left to concentrate on more important things.

Anyway, I immediately realised that I've used the same pattern in testing - with property initializers & test data 
builders. I've [posted before](@/blog/2009-04-10-the-test-data-builder-pattern-with-c-30.md) about Test Data Builders and I'd recommend you read that post first.

For small test data builder classes, it's really not that big a deal. For larger classes, using AutoMapper is quite useful. For example, for testing purposes we've got an exception details class that is sent over to an exception logging service.

Every time the app dies, we create an exception data transfer object, fill it out and then send it over the wire. When unit testing the service, I use a Test Data Builder to create the exception report so that I can vary its properties easily. Guess what? The test data builder's properties map 1:1 with the exception report - hmm!

So, rather than create the same boilerplate code to map the 10+ properties on the exception builder => data transfer object, I just used AutoMapper to handle the mapping for me :)

```cs
public class ExceptionReportDto
{
  public string ExceptionType { get; set; }
  public string StackTrace { get; set; }
  public string AssemblyName { get; set; }
  public string EntryPoint { get; set; }
  public string UserName { get; set; }
  public string MachineName { get; set; }
  // etc
}

public class ExceptionReportBuilder
{
  public string ExceptionType { get; set; }
  public string StackTrace { get; set; }
  public string AssemblyName { get; set; }
  public string EntryPoint { get; set; }
  public string UserName { get; set; }
  public string MachineName { get; set; }
  // etc

  // create the mapping when the static ctor is invoked
  static ExceptionReportBuilder()
  {
    Mapper.CreateMap<ExceptionReportBuilder, ExceptionReportDto>();
  }
}

public void ExceptionReportDto()
{
  // set up defaults
  ExceptionType = "System.ArgumentException";
  StackTrace = "Oh no I am a stack trace";
  //etc.
}

public ExceptionReportDto Build()
{
  // go go automagic!
  return Mapper.Map<ExceptionReportBuilder, ExceptionReportDto>(this);
 }
}
```

I've had good results with this approach. 

The only bit I'm remotely concerned about is creating the mapping in the static constructor. Any AutoMapper gurus out there who can say whether there's any reason I shouldn't do that?