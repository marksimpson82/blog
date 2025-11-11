---
id: 837
title: Jupyter Notebook to clean(ish) HTML
date: 2019-10-17T00:12:05+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=837
#permalink: /?p=837
tags:
  - dataviz
  - jekyll
  - jupyter notebook
  - notebook
  - overwatch
  - pandas
  - reddit
  - seaborn
---
I recently polled [/r/competitiveoverwatch](https://reddit.com/r/competitiveoverwatch) (aka /r/cow) users for their thoughts on [Overwatch](https://playoverwatch.com/en-gb/) with regards to fun and balance. It was well-received on reddit, so I thought I'd do a quick write-up on the pros & cons of using this approach.

You can [read the survey](https://defragdev.com/overwatch_surveys/2019_09/) and also check out the [code on github](https://github.com/marksimpson82/overwatch_survey).

## Overview

The survey was created with [Google Forms](https://www.google.com/forms/about/), which produces a raw results [Google Sheets](https://www.google.com/sheets/about/) spreadsheet. To analyse the data and generate the graphs, I used [pandas](https://pandas.pydata.org/) and [seaborn](https://seaborn.pydata.org/) in conjunction with [Jypyter Notebook](https://jupyter.org/), along with [Jekyll](https://jekyllrb.com/) to generate fairly clean HTML & CSS.

Most of the pertinent commands are in one place: [run_all.sh](https://github.com/marksimpson82/overwatch_survey/blob/master/run_all.sh)

### Step 1: Create the Google Forms survey

This was the most tedious part. While Google Forms is flexible, it also feels fairly clunky. On top of the general questions, I had to create 3 sets of questions per each Overwatch hero alongside the hero's image:

  1. Are they fun to play as?
  2. Are they fun to play against?
  3. Are they balanced?

If there was an easy way of exporting a survey's raw source (maybe JSON or XML), generating additional templated questions via a script and then re-importing it, I couldn't see it.

Instead, I created a self-contained Google Form that had the image & the three questions. I then imported this into the parent form, renamed the fields and updated the image... for ... all ... 31 ... heroes.

It was boring, but only took an hour of grunt work.

### Step 2: Export the responses from Google Sheets

After running the survey, I had a great response: 1200 players took the time to answer it.

Each Google Form has an associated Google Sheets results sheet. It's simple to export to CSV.

### Step 3: Create a more queryable data format

The original results .csv is a flat spreadsheet with 90+ uniquely-named columns like, "<span data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;I enjoy playing against Ashe&quot;}">I enjoy playing against Ashe</span>", and a rating between 1.0 & 5.0. This is pretty horrible for querying results, so I transformed the data into a more database-esque format: a single general responses table with a primary key, plus a hero responses table with a foreign key, hero name, response type ["playing_as", "playing_against", "balance" and "value"].

This is the sort of quick hackery that is a [joy to do](https://github.com/marksimpson82/overwatch_survey/blob/master/overwatch_survey/split_into_tables.py) in Python.

### Step 4: Create the notebook

Not much to say here. Pandas & Seaborn takes a bit of getting used to and there were a few transformations that I couldn't figure out using idiomatic Pandas code, but the development process was fairly painless.

I will say that there's a few practices that I found useful, though:

  * Avoid file-scoped operations. I tended to wrap my data crunching & graphing operations in functions, and avoided mutating data as much as possible.
  * Avoid using file-scoped variables as much as possible (it's easy to rely on or mutate something that will have side-effects).
  * Get in the habit of clearing all output & running all notebook cells.
  * If you're writing something that is useful to a reader, put it in a Markdown cell.

If I were creating a larger project with Notebook, I'd probably start making python modules & calling into them rather than spamming them into the main Notebook page. I.e. don't fall into the trap of treating Notebook files significantly differently to the usual way of writing Python code.

### Step 5: Strip unwanted elements

I didn't want to have the code front and centre, as the survey results were not intended for a technical audience - the Python would just get in the way. I tried writing a template for nbconvert to strip out the Python code, but couldn't get it working. Instead, I just wrote a quick 'n' dirty Python regex.

### Step 6: Use nbconvert -to markdown

Why Markdown? Well, I tried nbconvert -to html. While the results look pretty good at a glance, it generates a page with bloated, inline CSS (hundreds and hundreds of lines) along with base64-encoded images that are directly embedded in the HTML.

While this is great for a drag 'n' drop experience and for sharing intermediate results (there's no worrying about forgetting to include assets), it's not something I would be comfortable serving from my website.

The generated HTML was ~750KB, whereas a markdown variant came in under 270KB!

```bash
jupyter nbconvert --to markdown \
  overwatch_survey/analysis.ipynb --output-dir static_site
```

OK, so we have fairly clean Markdown, but now what?

### Step 7: Use Jekyll to generate HTML

Doing any kind of webdev install on Windows is a pain, but ... oh well. Jekyll is a solid choice and it works well. It also generates much better HTML for my purposes than nbconvert.<span class="pl-s"><span class="pl-pds"><br /> </span></span>

```bash
(cd static_site && bundle exec jekyll serve)
```

That's all I have to say about that.