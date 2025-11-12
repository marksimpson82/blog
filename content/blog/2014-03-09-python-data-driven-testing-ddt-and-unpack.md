+++
title = "Python data-driven testing, ddt and @unpack"
tags = ["python", "software", "testing", "tips"]
path = "/blog/2014/03/09/python-data-driven-testing-ddt-and-unpack.html"
+++
Several eons ago, [I wrote a blog post](@/blog/2012-05-21-data-driven-testing-with-python.md) about using 
the python ddt package. My only criticism was that you had to manually pack/unpack the test case arguments.

Happily, the developers of ddt were nice enough to add an @unpack decorator! You can now provide lists/tuples/dictionaries and, via the magic of @unpack, the list will be split into method arguments.

Documentation is here: [http://ddt.readthedocs.org/en/latest/example.html](http://ddt.readthedocs.org/en/latest/example.html "http://ddt.readthedocs.org/en/latest/example.html")