---
id: 848
title: Goodbye Wordpress, Hello Jekyll and Github Pages
date: 2020-08-02T00:00:00+00:00
author: Mark Simpson
layout: single
---

I've been using Wordpress with [34sp.com](https://34sp.com) hosting since the late noughties, and it's time for a 
change.

## Reasons for switching
I've got a few reasons for making the switch:
1. Wordpress is a permanent security and maintenance risk.

2. Authoring posts using markdown is a lot more pleasant & predictable.

3. [34sp.com](https://34sp.com) sadly withdrew their personal hosting product and forcibly migrated me to a professional one. 

In short, it's a clunk dev experience and fairly expensive.

## Making the switch
As with many web topics, it wasn't particularly difficult, but did involve a certain amount of head-scratching when 
mashing the various parts together.

### Create github repo(s) & enable github pages
If you're new to [github pages](https://pages.github.com/) like me, you'll possibly get confused by the fact that there 
are two types of github pages sites: `organisation` sites & `project` sites.

Organisation sites are limited to one per user or organisation, but you can have multiple project sites. 
 
I created two repos (caveat: I'm in 'just-make-it-work-mode', so exercise your own judgement):
1. [`<myusername>.github.io`](https://github.com/marksimpson82/marksimpson82.github.io) for my (2007!) root website 
content

2. [`blog`](https://github.com/marksimpson82/blog) for my blog 

The former will serve content for [https://defragdev.com](https://defragdev.com) & the latter for 
[https://defragdev.com/blog/](https://defragdev.com/blog/). For now, we'll leave them being served from 
[github.io](https://github.io), though. 

I found it a little confusing, but there's a convention whereby if you have a user/org repo with github pages enabled, 
further repos are served via subdirectory url schemes (i.e. hitting `yourdomain.com/X` will map to the contents held in 
repo `X`). 

As blog used to be served from [https://defragdev.com/blog](https://defragdev.com/blog), this worked fine for me.

### Export the data from wordpress
I followed a guide from [https://talk.hyvor.com/blog/migrate-from-wordpress-to-jekyll/](https://talk.hyvor.com/).

The gist:
* Install [jekyll-exporter](https://wordpress.org/plugins/jekyll-exporter/) on your wordpress site
* Enable it
* Export the data & download it (it may take a few minutes to generate the .zip)
* Disable it

This will give you the skeleton for your new jekyll-based site. 

### Install jekyll
I tried to install it using WSL and it didn't go very well(tm). Eventually got it working on Windows 10 directly, but I 
can't remember the exact steps I took. If you're using Mac or Linux, you'll likely have an easier time.

You can try to build the site via:
```bash
bundle exec jekyll serve
```

#### Fix wordpress ids (if needed)
If you're like me and your ancient wordpress scheme used integer post ids & query strings, then you're in 
for a treat -- it won't work. 

E.g. an old URL might look something like: `https://defragdev.com/blog/?p=50`

... which generates Front Matter like this:

```
---
id: 847
title: "Nvidia + G-SYNC - Black screen when alt-tabbing"
date: 2020-03-29T21:14:28+00:00
author: Mark Simpson
layout: single
guid: https://defragdev.com/blog/?p=847
permalink: /?p=847
---
```

The `permalink` doesn't work, as it's a query string (`jekyll serve` will fail with an obscure-looking error). 

If you have this problem, comment out all permalinks in your posts: 
```
#permalink: /?p=847
```

We'll come back to this later. If there's nothing else jiggered, the site should now build & serve locally.

### Choose an appropriate URL scheme
The default URL scheme seems pretty wordy to me, and will change the URL based on whether you add or remove categories 
or tags. While it does create a hierarchical navigation structure, I decided to jettison it for something simpler.

To do this, edit the `permalink` value in `_config.yml` and change it to something more succinct, like:
```
permalink: /:year/:month/:day/:title:output_ext
```

### Set up the [minimal mistakes](https://mmistakes.github.io/minimal-mistakes/) theme (optional)
[minimal mistakes](https://mmistakes.github.io/minimal-mistakes/) is a nice-looking theme, and was easy to configure. 

### Set up tag/category support (optional)
If you want to enable browsing by tags and/or categories, you'll need to do a bit more wrangling. This was the step that
probably caused me the most grief, as I couldn't easily understand what was built into minimal mistakes vs. the plugins
it integrated with.

You can either use something out-of-the-box (and potentially deal with some DRY-fail) or plump for a jekyll plugin.

In the end, I settled on [jekyll-archives](https://github.com/jekyll/jekyll-archives). However, there's a caveat: 
[jekyll-archives](https://github.com/jekyll/jekyll-archives) is not directly supported by github pages. 

I.e. If you go down this route, you'll need to handle building the site contents yourself. Fret not though, as it's 
fairly easy and covered in the next point!

### Set up github workflows to build the site (optional)
**Note**: If you're using plugins that are 100% compatible with github pages, you can skip this step. I'm using 
jekyll-archives, which is not supported.

The official [jekyll CI example](https://jekyllrb.com/docs/continuous-integration/github-actions/#setting-up-the-action)
 was simple to follow.
 
You'll need to create a secret with public repo access as per the guide.

For reference here's my version of 
[github-pages.yml](https://github.com/marksimpson82/blog/blob/master/.github/workflows/github-pages.yml)

Pushing to to `master` should now trigger a site build.

**Gotcha**: If you've not set up github pages for the repo, _nothing will happen_. You'll see the github action is 
present, but it won't do anything.

### Set up a redirection scheme (optional)
If you're migrating from wordpress then you'll want to keep your old URLs alive. There are various redirect plugins 
available for jekyll, so have a poke around. The front matter of each post should contain the old, exported URLs. 

#### The happy path
If your wordpress install was configured to use sensible URL schemes like `mysite.com/blog/why-parsnips-are-great/` then
you'll have no problem -- it's just a case of editing the front matter for each post and inserting the redirects. 

**Note**: If you have more than a handful of posts, I'd recommend writing a one-shot script to handle this.

#### The sad path (?query=strings)
My blog was unfortunately using an ancient URL scheme featuring integer ids and query parameters (e.g. `/blog/?p=123`) 
and this hobbles things somewhat. 

If you try to use a redirect plugin and configure it with something like 
`/blog/?p=123 => /2014-02-13/why-parsnips-are-great/`, it won't work (it'll crash when attempting to `jekyll serve`).

I went with a quick 'n' dirty solution yoinked from 
[danvk](https://github.com/danvk/danvk.github.io/commit/f99fa0d6ef808a2ba468587d3f7eab800d448f1e). It's a simple js file
that redirects via searching the current URL. It likely won't work with bots etc. but it'll do for now.

To populate it, I did the following:
```bash
grep -ri permalink _posts > /c/temp/guids.txt
```

Sample content:
`_posts/2008-11-08-assertthatpostcontent-textdoesnotcontainhello-world.md:#permalink: /?p=3`

I then wrote [a one-shot python script](https://gist.github.com/marksimpson82/fdc8f6915a6256391138fdc70a0a9a0b) to spit 
out the redirect line & pasted the lot into 
[redirect.js](https://github.com/marksimpson82/blog/blob/master/redirect.js).
 
### Set up a custom domain (optional)
Up till now, we've been browsing to a github pages URL. It's time to configure your custom domain (if you have one). 
I followed [this guide](https://medium.com/@hossainkhan/using-custom-domain-for-github-pages-86b303d3918a). 

In your github repo, create:
* A CNAME file (`Settings` > `GitHub Pages` > `Custom Domain`) (e.g. mine's set to `defragdev.com`)

On your host configuration (e.g. google domains or whatever you're using), create:
* A records to point to the github pages IPs
* A CNAME for `www.yourdomain.com`, if desired

DNS records can take up to 24 hours to cycle, but in practice it took an hour for mine to come through.

#### Automagic confusion
I stumbled due to something I mentioned earlier: I have a github org/user repo for my root site that uses github pages. 
I couldn't easily understand why [https://defragdev.com/blog](https://defragdev.com/blog) was magically being served 
without a CNAME being present. 

This is just a convention with github pages (read the start of this post). 

When I configured my [user repo](https://github.com/marksimpson82/marksimpson82.github.io) with a CNAME (pointing at 
`defragdev.com`), it indirectly means that project repos will be served as subdirectories -- as such, my `blog` repo 
is automagically served when I browse to [https://defragdev.com/blog/](https://defragdev.com/blog/).

This may or may not be what you want. It's perfect for me, but you may want to set up a subdomain of 
`blog.yourdomain.com` instead.

### Enforce HTTPS (optional)
I don't want to serve via HTTP, so I forced HTTPS. Check the box under:

`Settings` > `GitHub Pages` > `Enforce HTTPS`

### Fix up various content problems
Since I've been running every major version of wordpress since ~2008, the defaults have changed a lot over that time. As
a consequence, the exported content is quite changeable. 

If you've written a lot of posts, you're not going to have fun fixing up the content; in my own case it took about 4
hours to fix up my paltry 87 posts. The low number of posts and changeable formatting meant that it wasn't worth 
automating, so I went with occasional scripts, grep & targeted manually editing.

Some of the problems/fixes include:

#### Broken internal blog links
While my hacky redirect solution worked, it's obviously better if you can use the built-in Jekyll functionality to 
create internal links.

**Fix**: see [Jekyll: linking to posts](https://jekyllrb.com/docs/liquid/tags/#linking-to-posts). The `post_url` 
syntax is handy, as `jekyll serve` will fail with an error message if you have a broken internal link. 

#### Text content and formatting issues
My blog's content was all over the place and included a mixture of markdown, html etc.

**Fix**: manual editing

#### Code snippets
Code snippets were similarly in a mixture of formats, all of which won't play nicely with markdown.
 
**Fix**: see [Jekyll: code snippets](https://jekyllrb.com/docs/configuration/markdown/#redcarpet) -- this involved a lot of 
manual editing, but was a doddle compared to the bad old days of wordpress formatting.

#### Special characters & entity names/numbers 
These either hinder readability while editing posts (e.g. `&lt;` aka `&#60;` for `<`, `&gt;` aka `&#62;` for `>`) and/or 
don't render correctly in a browser (`<pre>` combined with `&nbsp`).

If you have a lot of content, it'd probably be wise to ignore entity names/numbers that render correctly in the 
browser and focus on the legitimate content problems.
  
**Fix**: I fixed these problems via search/replace mostly -- be careful as sometimes the context means that the entity 
names/numbers are required (or may require escaping or different quotes if removed).

#### Irrelevant tags like `<--more-->`
**Fix**: Search & delete.