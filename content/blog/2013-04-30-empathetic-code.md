+++
title = "Empathetic Code"
tags = ["api", "design", "software", "tips"]

+++
I always liked the phrase, “if you’re incapable of empathy, then you shouldn’t be designing APIs”.

I’ve worked with some terrible libraries in the past and the worst ones all had a common design flaw: the author didn’t put themselves in the user’s place. Worse still, sometimes the author _just didn’t give one_. When someone using the code pointed out that something was hard to understand or didn’t make sense, they were met with a snarl and shouted down; “it makes sense; you’re just using it wrong”.

On the other hand, I’ve occasionally picked up libraries/frameworks that make an extra effort to guide you along the correct path. The author of the code understood where users were likely to stumble.

[<img title="image" style="border-top: 0px; border-right: 0px; background-image: none; border-bottom: 0px; padding-top: 0px; padding-left: 0px; margin: 0px; border-left: 0px; display: inline; padding-right: 0px" alt="image" src="https://defragdev.com/blog/images/2013/04/image_thumb.png" width="244" height="190" border="0" />](https://defragdev.com/blog/images/2013/04/image.png)

It doesn’t matter whether it’s a carefully designed API you’re crafting for external use or internal code that will only be viewed and modified by engineers inside the company, you can always do something extra, especially if it’s something that’s already tripped you up.

If you encounter a gotcha, why not write a bit of code to clearly document the case, particularly if it is time-consuming to debug in the first place?

## Debugging may diagnose problems, but...

When I was writing some road graph parsing code, due to the way that shapefiles are delivered by certain vendors, it was possible that the same road edge could be added twice. The road edges had the same ids / properties, but appeared in multiple files (files A and B contain contiguous geographical areas; roads crossing from A to B or vice-versa are sometimes contained in both files). This then caused some of the angle calculation code to detonate as, unsurprisingly, intersections between parallel lines don’t tend to give sensible results. Hi, NaN.

Initially it just looked like some of the maths code was wrong, but working my way back, I eventually figured out that it was caused by failing to handle the input data correctly, as we did not anticipate that duplicate edges could exist.

The moment I realised the root cause, I added some code that ensured that no duplicate edges could be added to a single junction. If this happened, an exception would be thrown with the junction id, the existing road edge ids and the road id that was being added. My colleague then fixed the problem upstream in the vendor data parsing such that duplicates were filtered out.

A few months later we received data for a new territory from a different vendor. Guess what? It had the same problem. However, this time around when my colleague tried to run the process, it told him exactly what was wrong. If I hadn’t added the consistency check (which took all of 5 minutes), the chances are that I would’ve forgotten what the issue was and had to go deep-dive debugging again.

Debugging stuff (especially long-running processes that crunch lots of data) can be time-consuming and difficult. Once you understand the root cause of a problem, adding consistency checks that detect specific, known problems is comparatively easy. It also protects against [the bus factor](https://en.wikipedia.org/wiki/Bus_factor). If you spend an hour debugging a situation that can potentially happen again, adding a little code to detect the issue is a sensible thing to do.

## Fail helpfully

OK, so you’ve detected a problem and bailed out, but you can do better. If you’ve hit this snag before and have a suggestion or two as to what the root cause is likely to be, say so.

E.g. I had quite a few cases in Python where a function was meant to be passed to a constructor as an argument, but I accidentally invoked the function and passed the result, instead. A good bit down the line, you’d get some error or other that ‘list is not callable’.

I managed to catch myself out a few times, so what’s someone else going to make of this? How can we improve it?

```python
def __init__(self, create_func):  
  if not callable(create_func):  
    raise ValueError("create_func was not callable. Did you accidentally invoke the function instead of passing it as an argument?")
```

Sometimes it’s very small things like this that can make a big difference. If someone makes this mistake, they know exactly what to do to fix it. Compare this to running some unfamiliar code and being confronted by a stack trace 20 fathoms deep, where a value that was set eons ago was invalid.

## Show ‘em what you got

If a user has to pass some arguments, put configuration files in a conventional location or select options from a list of known/registered things etc. it is very helpful if you can show the user what the program is aware of.

Imagine we’re creating a tool whose configuration is conventional. Tasks are defined in code. Each task definition must have a matching configuration named in the form <taskname>.conf.

The user wants to run the colour task.

```bash
run.exe colours
```
```
Output:

Error. Couldn’t find file. Exiting.
```

-versus-

```bash
run.exe colours
```

```
Output:

Error running task 'colours'. Cannot find the required configuration file 'colours.conf'.
 
Registered configuration files:  
- colors.conf  
- terrain.conf  
- disco.conf
 
Suggestions:  
- Did you create a configuration file yet?  
- Is the configuration named correctly? It should be in the form 'taskname.conf'. Perhaps you made a typo?
```

The user has a much better chance of realising their error when things are shown to them in this manner.

## Don’t fail, only to fail again!

Imagine you had a compiler that told you about precisely one warning or error. That’s your whack. You run the compiler, get the error message and then fix it. You compile again. It spits out a new error. You fix that. You compile again. Repeat ad nauseum until they’re all gone.

If this sounds terrible and you’re shaking your head, then why is it so common to find this pattern in program design?

If it is possible to collect _all_ of the errors before failing (or at least all of the errors that occurred during a particular _phase_), then do so! Compilers do this. Test runners do this. Various other bits of software do this, and yet it is not something a lot of folk think about.

Here’s what you need to collect errors (pseudo C# – close enough)

```cs
public class ErrorMessageBuilder  
{  
  private StringBuilder m_errors = new StringBuilder()

  public void AddError(string message)  
  {  
    m_errors.AppendLine(message);
  }

  public bool HasErrors { get { return m_errors.Count > 0; } }  
}
```

Pretty complicated, ja? Instead of immediately killing the program when an error occurs, simple whack it into the error message builder. Once a particular phase is complete, check to see if it has anything in it. If it does, then call its ToString() method and die.

Your users can now fix multiple errors in one go before re-running your tool. Again, this is a very, very small change, but can make things a lot nicer, particularly for tools that have a significant bootstrap / run time.