---
title: "understanding jj's branching and bookmarks"
date: 2026-08-16T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - jj
  - git
  - vcs
  - scm
---

## What is `jj` aka jujutsu?
[`jj`](https://docs.jj-vcs.dev/latest/) is a git-compatible version control system (VCS) that has fewer primitives, commands and moving parts, and yet feels like it offers you just as many options as git, if not more.

I've been playing with it on and off since late 2025, and have now fully swapped over. Why? Well, I've been using git since ~2011 and, as well-versed as I am in git-fu, it's still not particular ergonomic. 15 years of using one VCS is a good run. `jj` already feels like a big improvement.

## Can I use `jj` instead of git?
Possibly. `jj` may not be suitable if you work in git repositories that:
- [Make extensive use of submodules](https://github.com/jj-vcs/jj/issues/494) (for occasional operations, you can fall back to git)
- [Use a `.gitattributes` file](https://github.com/jj-vcs/jj/issues/53)
- Are very large (hasn't yet been an issue for me)

I've worked on many projects where `jj`'s lack of `.gitattributes` support would scupper things, so I'm hoping they can at least roll out `eol` support :-)

I'm not going to write yet another `jj` how-to guide in this post, as there are many great ones already out there. Instead, I'm going to focus on the mental leap I failed to make.

## What's with the branching and bookmarks? I don't get it
The main conceptual difference between `jj` and git is the way to think about branching. `jj` supports branching and naming said branches, but it's got a few subtle differences. I personally struggled to see things clearly. After 15 years of git, I was viewing `jj`'s world through git goggles.

Before I talk about `jj`, let's recap how git branching works.

## git branching
Firstly, what is the technical definition of a git branch? [The git book](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) roughly says that a branch is:
> A lightweight, movable pointer to a commit

Hmm, that's pretty terse. What does it mean? Let's examine the files in the hidden `.git` directory to find out: if you look in the `.git/refs/heads` directory, you'll see a text file per branch:

```shell
$ ls .git/refs/heads
a_feature b_feature main
```

Printing out `main`'s contents:

```shell
$ cat .git/refs/heads/main
0ac0576629de05883afc22db5af2e664af12e25c
```

Which, lo and behold, matches the commit of my `main` branch:

```shell
commit 0ac0576629de05883afc22db5af2e664af12e25c (HEAD, origin/main, main)
Author: Mark Simpson
    fix title
```

In git technical land, a branch is little more than a pointer to a commit. When you create a branch, switch to it and create a commit:
1. A new commit node is appended to the [Directed Acyclic Graph (DAG)](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
1. The new node's parent pointer is linked to the previous commit 
1. The `.git/refs/heads/<$branch_name>` file is automatically updated with the tip's commit hash*

***Note**: This is a bit of a simplification, as git 2.45 onwards contains an optional way of storing refs -- via an optimised [reftables implementation](https://about.gitlab.com/blog/a-beginners-guide-to-the-git-reftable-format/), so if you don't see anything in your `.git/refs/heads/` dir, that's probably why.

git starts from the leaf level (storing the commit hashes of all branch tips) and works its way backwards through the DAG. It does not store bidirectional links between commits; git cannot walk the graph from the root. It can only walk backwards from the leaves. Consequently:
- Finding the root commit is an `O(N)` operation
- Finding the tip of a branch is an `O(1)` operation

As a corollary of needing to 'work backwards' from branch tips is that if you ever `git checkout` a commit hash, you move into a `detached HEAD` state and get this scary-looking message:

```shell
$ git checkout ab711

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch
```

While you _can_ make new commits while in a detached HEAD state, the new commits may become unreachable. Why? Let's say we have the following repo state:

```
m1  m2  m3*
o---o---o branch: main
         \
          f1  f2*
          o---o branch: feature
```

If we `git checkout f1`, then make a new commit, we get something like:

```
m1  m2  m3*
o---o---o branch: main
         \
          f1  f2*
          o---o branch: feature
           \
            d64e2b9
             o  branch: none (unreachable)
```

git has modified the DAG, and while we have created a fork in the DAG _without_ using a `branch` or `switch` command, git doesn't yet have a permanent reference to commit `d64e2b9` (there is no file referencing it in the `.git/refs/heads/<$branch_name>` dir).

Indeed, if we `git switch main` after creating commit `d64e2b9`, we get a warning message:

```shell
$ git checkout main
Warning: you are leaving 1 commit behind, not connected to
any of your branches:

  d64e2b9 my sort-of-branched commit that will become unreachable

If you want to keep it by creating a new branch, this may be a good time
to do so with:

 git branch <new-branch-name> d64e2b9
```

Anyway, so far, so dry. We've learned that:
1. Branches are both simple & cheap to maintain
1. Git branching involves the mutation of the DAG **and** the auto-advancement of the branch pointer when committing. 
1. You can create branches in the DAG _without_ moving the branch pointer, but it's not idiomatic

So far, so unremarkable. So why did `jj` confuse me?

## `jj` branching
A branch in `jj` is implicit in the topology of the DAG. If a commit has multiple children, we're branching! Here's a simple example of a `jj` repo containing a few commits:

```shell
$ jj log
@  loqysznv me@example.com 2026-08-08
│  (empty) wip: another thing
◆  qupzqmym me@example.com 2026-07-25
│  fix title
```

It's looking linear and non-branchy. Let's change that.

In `jj`, the new `new` command creates a commit and modifies the DAG. The `new` command takes an optional parent commit (which defaults to the current commit if none is specified). If the nominated parent commit already has a child, we get a branch! Let's create a branch by using the `qupzqmym` ("fix title") commit as the parent:

```shell
$ jj new -r qupzqmym -m "ey we're branching!"

$ jj log
○  xxourlut me@example.com 2026-08-18
│  jj: bookmarks and branches
│ @  znvuuoup me@example.com 2026-08-19 <--- new commit
├─╯  ey we're branching!
◆  qupzqmym me@example.com 2026-07-25 <--- parent commit now has 2 children
│  fix title
```

Because commit `qupzqmym` now has two children, we've created a branch. It's just that easy.

Similarly, if we want to merge branches, we run `jj new` while providing two or more commit ids. This is an example of `jj`'s simplicity: one command can branch _and_ merge (and it's not some weird `git checkout`-style command that does unrelated things). As an added bonus, there's no need to remember which branch you're 'on', or in which direction you're merging, either: just look at the DAG, call `jj new` and provide the correct parent IDs.

You might be thinking, "err, without branch names, won't the git commit hashes change as we edit the commit contents/messages/parents, making it impossible to keep track of things?" Happily, each underlying git commit is paired with a `jj` [`Change ID`](https://docs.jj-vcs.dev/latest/glossary/#change). No matter how many times you edit or rebase a commit, its `Change ID` remains the same:
> A change ID is a unique identifier for a change. They are typically 16 bytes long and are often randomly generated. By default, jj log presents them as a sequence of 12 letters in the k-z range, at the beginning of a line. These are actually hexadecimal numbers that use "digits" z-k instead of 0-9a-f.

This is one of `jj`'s best features. Stability is a huge plus when editing history. The DAG combined with immutable `Change IDs` is often enough to differentiate work streams and keep track of things.

So, that's branching in `jj` and we haven't even talked about ...

## `jj` and `bookmarks`
So if we're able to branch and track changes without ever typing the words `branch` or `switch`, what _are_ `bookmarks`? Well, `jj` is built to work with multiple [`backends`](https://docs.jj-vcs.dev/latest/glossary/#backend), but git is currently the only workable backend:
> A backend is an implementation of the storage layer. There is currently only one production-ready builtin commit backend: the Git backend. The Git backend stores commits in a Git repository...

If we want to share our work via a forge like GitHub/BitBucket/Codeberg etc. then we need to use git's lingo. Git's lingo is branches, and `jj` achieves this via `bookmarks`.

`jj` `bookmarks` are ... you guessed it, a movable pointer to a commit. At a technical level, it looks spookily like git. In fact, if you look at the underlying `.git/refs/heads` dir after creating a `jj` `bookmark`, you'll see the exact same named file containing a git commit hash. At a technical level, they are equivalent to git branches.

So what's actually different? The main difference is that `jj` `bookmarks` _behave_ differently as you use the cli -- they're more like a sticky post-it note you slap on a particular commit after the fact.
1. They do **not** automatically advance as you create new child commits
1. But they do move with changes when editing history (e.g. rebasing)

At the interface level, instead of actively 'switching' to a branch or being 'on' a branch, you create `Changes`. Once you have a `ChangeID`, you can slap a `bookmark` on it. Let's take our previous example:

```shell
$ jj log
○  xxourlut me@example.com 2026-08-18
│  jj: bookmarks and branches
│ @  znvuuoup me@example.com 2026-08-19 <--- we're going to bookmark this
├─╯  ey we're branching!
◆  qupzqmym me@example.com 2026-07-25
│  fix title
```

Let's create a `bookmark` called `feature_b` and slap it on change `znvuuoup`

```shell
# shorthand: `jj b c -r zn feature_b`
$ jj bookmark create -r znvuuoup feature_b
$ jj log
○  xxourlut me@example.com 2026-08-18
│  jj: bookmarks and branches
│ @  znvuuoup me@example.com 2026-08-19 feature_b <--- new bookmark
├─╯  ey we're branching!
◆  qupzqmym me@example.com 2026-07-25
│  fix title
```

Again, it's just a git branch under the hood.

```shell
$ ls .git/refs/heads/
feature_b

$ cat .git/refs/heads/feature_b
95b2cb93dcb7feb4101468481b1ff487dddb4e5b
```

Now, let's create a change that's a child of change `znvuuoup` aka `feature_b` and start editing it (the default behaviour unless the `--no-edit` is specified):

```shell
# we could also do this via jj new -r znv -m "new commit on branch"
$ jj new feature_b -m "new commit on branch"

$ jj log
○  xxourlut me@example.com 2026-08-18
│  jj: bookmarks and branches
| @  xmnqnsrx me@example.com 2026-08-19 <--- new change we just added
| │  new commit on branch
│ ○  znvuuoup me@example.com 2026-08-19 feature_b <--- bookmark `feature_b` stays at old change!
├─╯  ey we're branching!
◆  qupzqmym me@example.com 2026-07-25
│  fix title
```

We can see that the user interface is different to git: when we created a new commit whose parent was the `bookmark` `feature_b`, it did **not** modify the bookmark -- it stayed put.

If we want to move the `bookmark`, it is a deliberate action:
```shell
# you can also use `jj bookmark advance` aka `jj b a` to do this
$ jj bookmark move feature_b --to xmnqnsrx
```

Because we understand that a bookmark is just a git branch, and a branch is just a pointer to a commit, it makes intuitive sense that bookmarks can be moved around arbitrarily, just like a post-it note.

## Other mental hurdles -- my brain is biased to prefer straight lines
Due to initially viewing `jj` through git goggles, my mind plays tricks on me when I look at the DAG.

E.g. let's say we have a repository where we have a `main` bookmark on `ChangeID` `lys`, and we've created two child changes from `lys` like so:

```shell
$ jj new -m "childA" --no-edit  # creates change pol
$ jj new -m "childB" --no-edit  # creates change ghr
```

A messy visualisation of the DAG:

```
z (root)                lys ("blah") main*      pol ("childA")
o-----------------------@-----------------------o
                         \
                          o ghr ("childB")
```

Either of those changes are valid candidates for the `main` bookmark's next move. However, my grug brain looks at this DAG and instinctively thinks `main` will advance to commit `pol`. This is just a daft side-effect of the way the graph is drawn -- my brain sees a straight line from `z` -> `lys` -> `pol` and thinks that's the natural progression. However, I could equally draw the graph like this by swapping the two changes:

```
z (root)                lys ("blah") main*      ghr ("childB")      
o-----------------------@-----------------------o
                         \
                          o pol ("childA")
```

To counter this, I try to think about the DAG like this:

```
           o pol ("childA")
          /
z        /  
o-------o lys ("blah") main*     
         \
          \
           o ghr ("childB")
```

This fixed things for me. I can instantly visualise that there are two equally valid choices to advance the branch.
