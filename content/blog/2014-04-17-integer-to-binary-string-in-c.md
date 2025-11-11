+++
title = "Integer to binary string in c#"
tags = ["binary", "bitwise", "c#", "decimal", "python", "tips"]
+++
Python has the terribly useful functionality of [bin()](https://docs.python.org/2/library/functions.html#bin) to do this, but what about C#?

On the rare occasion I have to monkey around with bitwise operators, I always keep this handy. It has the added bonus of printing the leading zeros – I find this very useful when writing/debugging bitwise code, as it makes it easy to line up bitmasks etc. in the immediate window / console.

```cs
public static class BinaryPrinter  
{  
 public static string ToBinaryString(long _long)  
 {  
 // have to do this or it won't print the leading 0 values  
 return Convert.ToString(_long, 2).PadLeft(sizeof(long) * 8, '0');  
 }  
}
```
Similarly, you could write a few of these (for all of the various inbuilt types) and chuck them in extension methods.