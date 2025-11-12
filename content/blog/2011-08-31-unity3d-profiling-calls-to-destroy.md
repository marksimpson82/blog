+++
title = "Unity3d - Profiling calls to Destroy"
tags = ["c#", "debugging", "software", "tips", "Unity3d"]
+++
## Destroy All ... Things

I've recently been investigating some performance problems in our Unity3d app. In one specific instance (running full screen on a rubbish laptop), there were numerous large performance spikes caused by the nebulous-sounding "Destroy". After prodding a little bit, Destroy is related to calling [GameObject.Destroy()](http://unity3d.com/support/documentation/ScriptReference/Object.Destroy.html).

Unfortunately, Unity3d's profiler won't give you any information related to what types of objects are being destroyed, and wrapping your GameObject.Destroy calls in profiler sections doesn't help, as Unity3d defers the work for later in the frame (so the methods return nigh-on immediately). As such, you get told "Destroy is taking x ms this frame", and that's about it.

## Finding the culprits with the profiler

I managed to work around this limitation by (temporarily) changing all GameObject.Destroy() method calls to [GameObject.DestroyImmediate()](http://unity3d.com/support/documentation/ScriptReference/Object.DestroyImmediate.html) then wrapping the calls in [Profiler.BeginSample()](http://unity3d.com/support/documentation/ScriptReference/Profiler.BeginSample.html) / Profiler.EndSample() pairs.

**Note:** If you access your unity instances in the same frame after calling destroy, this probably won't work for you.

It was then possible to see which resources were doing the damage on the laptop. All of our resource cleanup code was in one place, so it was trivial to do.

The temporarily instrumented code ended up looking something like this, and immediately let us know the culprits. Note this code is just a simplified mockup, but it should give you the gist of the idea:

```cs
// centralised resource cleanup makes profiling simple 

private void CleanupResources<TResource>() { 
  Profiler.BeginSample("Destroy: " + typeof(TResource).Name); 
  IEnumerable<TResource> resources = 
    FindResourceOfType(typeof(TResource)); 

  foreach(var resource in resources) 
  { 
    resource.Dispose(); 
  } 

  Profiler.EndSample(); 
}
 
//... and each Resource type inherits from a common base class 
// implementing IDisposable. 
public abstract class Resource : IDisposable 
{ 
  protected abstract void CleanupUnityResources(); 
 
  public void Dispose() 
  { 
    CleanupUnityResources(); 
  } 
}

public class SomeResource : Resource 
{ 
  private Mesh m_unityMesh; // gets set when resource is locked in 
 
  protected override void CleanupUnityResources() 
  { 
    // GameObject.Destroy(m_unityMesh); 
    GameObject.DestroyImmediately(m_unityMesh); 
  } 
}
```