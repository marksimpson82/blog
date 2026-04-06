---
id: 761
title: "Python 3.4 and the three P's: pyvenv, pip & pycharm"
date: 2014-03-23T21:33:29+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=761
#permalink: /?p=761
tags:
  - pip
  - pycharm
  - python
  - pyvenv
  - venv
  - virtualenv
---
## Pip

... is a nice little package manager for Python, but it was somewhat hamstrung by the clunky install procedure in Python 2.X and early versions of Python 3. With Python 2.x, you’d have to do something like use curl to get setuptools, then use easy install to get pip, then use pip to install packages. Happily, 3.4 now includes pip by default.

## Pyvenv

... is a virtual environment manager. Rather than installing packages in your site-packages directory (modifying your python environment – something that is a bit sucky when you have conflicting needs for different projects), developers have traditionally used virtualenv. In Python 3.X, you can use pyvenv instead and it seems to Just Work&#x2122;.

## All Together Now

On Windows, getting pip and pyvenv working together is pretty simple, but I had a little trouble finding the bare minimum “getting started” documentation, so here’s a version for frantic googlers.

First, set up a virtual environment using pyvenv:

Open a command prompt in the directory you’d like to create the virtual environment, then run the following command:

```
python C:\your_python_dir\Tools\Scripts\pyvenv my_env_name
```

Then, run:

```
my_env_name\Scripts\activate.bat
```

This will give you a command prompt with the environment name prepended to signify that it’s active.

At this point, you can start installing stuff with pip!

```
pip install beautifulsoup4
```

![Installing beautifulsoup with pip]({{ '/assets/images/2014/03/pip_install.png' | relative_url }})

Not bad. Much simpler than in olden times.

## A bonus – PyCharm & pyvenv

[PyCharm](https://www.jetbrains.com/pycharm/) is my IDE of choice for python editing and it comes with a lot of niceties, including allowing you to associate projects with specific python interpreters. Even better, PyCharm allows you to associate a project with a particular virtual environment, too!

I’m running v3.0 of PyCharm at home, so I can’t speak for earlier versions. To associate a virtual environment with your project, click File –> Settings, then find “Python Interpreters” under “Project Interpreter”.

![pycharm env editor, showing executables]({{ '/assets/images/2014/03/pycharm_interpreter.png' | relative_url }})

Click the + at the top right hand pane of the window, then select “Local”. Navigate to the virtual env directory you just created, then find the Python executable under the scripts dir.

![pycharm, selecting the interpreter]({{ '/assets/images/2014/03/pycharm_interpreter2.png' | relative_url }})

You can now associate this virtual environment with your project. PyCharm automatically switches it up when you load your projects. No more cross contamination of packages!
