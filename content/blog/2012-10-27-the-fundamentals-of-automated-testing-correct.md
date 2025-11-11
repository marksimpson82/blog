+++
title = "The fundamentals of unit testing: Correct"
tags = ["fundamentals of unit testing", "testing", "tips"]
+++
This post is [part of a series](@/blog/2012-10-24-the-fundamentals-of-automated-testing-series.md) on unit testing.

Once you’ve decided what you’re going to test, chosen a good name and started to write the code, the next step is to make sure that the test is purposeful and correct. This is a simple tip and largely common sense.

## Does the test code’s functionality match its name?

It is simple to accidentally write a test that purports to test one thing, but actually tests another. E.g. 

```cs
[Test]  
public void model_is_loaded_correctly_from_stream()  
{  
 // Arrange  
 var resourceLoader = CreateResourceLoader();  
 var modelDataStream = CreateModelDataStream();

 // Act  
 var loadedResource = resourceLoader.LoadFromStream(modelDataStream); // fine so far

 // Assert  
 Assert.That(resourceLoader.LoadedResources, Is.EqualTo(1)); // buh?!  
}
```

In this test, we can see that it claims to test that loading a model from a stream returns a valid resource. However, the test is then asserting that the loaded resources count has increased. It is not checking the returned resource for correctness. Either the test name is out of date, or it is not testing the correct thing. 

If it is the former case, we should rename the test to “loading a model increments the loaded resources count”. If it is the latter case, we should change the test such that we are asserting on the model’s state. How do you know the model has been loaded correctly if you’re not inspecting its vertices, indices and UVs?

If we are misled by our test names, it is irritating because it looks like something is covered, but it’s not. If we’re asserting on the wrong stuff, then our test won’t save us when the unit of code malfunctions. Maybe it’s already bugged.

## Is the Assert meaningful?

All tests should assert against some meaningful result. Put simply, if a test does not prove much, then it is not worth writing or maintaining.

Here is an example of a test that looks useful but, on closer inspection, is doesn't really prove much at all. 

```cs
[Test]  
public void game_properties_are_correctly_serialized()  
{  
 // Arrange  
 var currentLevel = 4;  
 var playerName = "Steve";  
 var game = CreateGame(playerName, currentLevel);  
 var serializer = CreateGamePersistence();  
  
 using(Stream stream = new MemoryStream())  
 {  
 // Act  
 serializer.Save(game, stream);  
 }  
  
 Assert.That(true, Is.True) // WHAT?!?!?  
}
```

I’ve seen the `Assert true == true` anti-pattern numerous times. If the assert is missing or tells us nothing useful, the chances are the test isn’t going to prove much, so why are some developers compelled to do it? My guess is that people think, “hmm, I’ve written a test with no asserts, there we go”. If you ever get tempted to do this, don’t! It’s a sign that something is wrong.

**Note**: it’s sometimes useful to have methods like this to act as surrogate Main() methods so we can invoke them via a test runner for easy debugging but, in general, it’s not a terribly good idea and you wouldn’t want to run these tests as a part of your normal development workflow.