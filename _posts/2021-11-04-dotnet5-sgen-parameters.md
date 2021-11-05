---
title: "Parameterising sgen (aka the .NET Microsoft.XmlSerializer.Generator) via a .csproj PropertyGroup"
date: 2021-11-04T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - sgen
  - Microsoft.XmlSerializer.Generator
  - dotnet
  - csharp
---

## The problem
If you've landed on this post via searching the web, you probably already know what sgen.exe is, and what the 
[`Microsoft.XmlSerializer.Generator`](https://docs.microsoft.com/en-us/dotnet/core/additional-tools/xml-serializer-generator) 
nuget package does. 

You probably used to [invoke sgen](https://docs.microsoft.com/en-us/dotnet/standard/serialization/xml-serializer-generator-tool-sgen-exe) 
as part of a build script or a post-build .csproj step and parametrise it as you saw fit: e.g. passing `/type:MyType` to
limit it to a single type. 

Sgen has historically been flaky to use (as it changed location on disk depending on which Windows SDK was installed 
and some other factors), so it's great it's now done via a nuget package. That's the good part.

The bad part is that since switching to the 
[`Microsoft.XmlSerializer.Generator`](https://docs.microsoft.com/en-us/dotnet/core/additional-tools/xml-serializer-generator) 
nuget package, you're thinking: "How do I pass arguments to sgen now that it's automagically invoked via `dotnet build`?" 
and also "where is the documentation?"

I had the same reaction, dear reader. Porting an old C# project to [.NET 5](https://dotnet.microsoft.com/download/dotnet/5.0) 
resulted in sgen exiting with an error, as the default behaviour tries to generate serializers for every type in the 
target assembly. I don't want this behaviour for a few reasons:

1. It generates code I don't want or need (and a bulkier serialization assembly)
2. It fails if namespacing is required (Got an assembly containing `NS1.Triangle` & `NS2.Triangle`? Sgen will 
fail unless you disambiguate the types via namespacing)

We can fix both issues by simply telling sgen "hey, only generate serialization types for `/type:MyType`". Only now we 
can't, because `Microsoft.XmlSerializer.Generator` is calling the shots rather than us directly calling sgen.

## The answer!
Blessed art thou, because it wasn't even possible until 2019 (which seems like an oversight). 
The answer is in the GitHub [Pull Request](https://github.com/dotnet/corefx/pull/36085) that added this functionality. 

I haven't been able to find any official documentation, so this is all we have to go on.

1. Open the .csproj containing the serialization types 
2. Add a `PropertyGroup` section
3. Set one of the properties, using the attribute naming format of `<SGenParamName>`, where "ParamName" is a parameter name gleaned from the
[sgen documentation](https://docs.microsoft.com/en-us/dotnet/standard/serialization/xml-serializer-generator-tool-sgen-exe#parameters)
   - E.g. `type` would become `<SGenType>`
4. Save the project & then build as normal. 

Here's the example XML from the [PR](https://github.com/dotnet/corefx/pull/36085) by `jiayi11` (thank you, kind fellow): 
```xml
<PropertyGroup>
    <SGenReferences>C:\myfolder\abc.dll;C:\myfolder\def.dll</SGenReferences>
    <SGenTypes>SgenTestProgram.MyType1;SgenTestProgram.MyType2</SGenTypes>
    <SGenProxyTypes>false</SGenProxyTypes>
    <SGenVerbose>true</SGenVerbose>
    <SGenKeyFile>mykey.snk</SGenKeyFile>
    <SGenDelaySign>true</SGenDelaySign>
</PropertyGroup>
```
For my use-case (serialization of a single type in a single project), all I needed to add was:

```xml
<PropertyGroup>
    <SGenTypes>Tools.Blah.MyClass</SGenTypes>    
</PropertyGroup>
```
That's it!

## A bonus tip
The documentation for the 
[`Microsoft.XmlSerializer.Generator`](https://docs.microsoft.com/en-us/dotnet/core/additional-tools/xml-serializer-generator) 
doesn't seem to be 100% up to date for .NET 5 (and .NET 6 is due any day now, too!)

If you're running with .NET 5, rather than copying the docs that suggest:
```bash
dotnet add package Microsoft.XmlSerializer.Generator -v 1.0.0
```
&
```xml
<ItemGroup>
   <DotNetCliToolReference Include="Microsoft.XmlSerializer.Generator" Version="1.0.0" />
</ItemGroup>
```

... you can the command & XML version to `=5.0.0` to get the latest version.

## Read on for some background
Anyway, I've hopefully saved you some head-banging.

For the rest of you that don't know what sgen is and are vaguely interested, here's a short explanation (warning: 
this is boring, but it's also useful to know for anyone doing XML serialization).

## sgen.exe
Sgen is an XML serialization code generator. For a given assembly and (optionally) a type that you want to serialize, it 
generates a .dll containing the serialization code **at compile-time**.

Let's say you have a toy project like so:

    project_root
    ├── MyApp.sln    
    ├── MyConsoleApp
    │   ├── MyConsoleApp.csproj
    │   ├── Program.cs
    ├── MyClassLibrary
    │   ├── MyClassLibrary.csproj
    │   ├── NeedsXmlSerialized.cs

Our class `NeedsXmlSerialized.cs` needs to be serialized to Xml (or deserialized) during the course of the app run.

```c#
public class NeedsXmlSerialized 
{
  public int SomeInt { get; set; }
}
```

In our Program.cs, we use the `XmlSerializer` class to convert our `NeedsXmlSerialized` instance to XML:

```c#
public class Program 
{
  public static void Main() 
  {
    var serializer = new XmlSerializer(typeof(NeedsXmlSerialized));
    using(var writer = new StreamWriter(@"C:\some\file.xml"))
    {
      var typeToBeSerialized = new NeedsXmlSerialized;
      typeToBeSerialized.SomeInt = 5; 
      serializer.Serialize(writer, po);
    }
  }
}
```

OK, so far so good. The program works, and we've not even mentioned sgen yet.

## If it works already, why use sgen?
The short answer is performance. If the serialization types have not yet been generated, they must be created 
on-the-fly at **run-time**. I.e. the first time you want to serialize/deserialize your class to/from XML, there is a 
constant (and large!) stall. The serialization types are then cached & re-used for the rest of the run, but the 
down-payment can be considerable.

I've seen this in production and it's not pretty, especially in pathological cases where the runtime is short-lived and 
only does one bout of serialization, e.g.: 
* The program starts up (20ms)
* It does some CPU-bound work (300ms)
* XML serialization types are generated on the fly (350ms)
* Serialize to XML (20ms)
* The program exits (5ms)

In this case, we spend around half of the program's runtime generating the serialization types each and every run. This 
is scandalously wasteful. If you were to gaze at the profiling data, you'll see a monolithic block of waste that seems 
to be non-app code.

An even better thing to do is avoid XML serialization and do something else instead. In my case we have no choice, as 
the file format is sadly non-negotiable.
