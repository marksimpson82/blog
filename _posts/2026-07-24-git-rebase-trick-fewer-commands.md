---
title: "git trick -- git fetch origin main:main"
date: 2026-07-24T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - git
  - rebase
  - vcs
  - scm
---

## Git rebase basics
A decent percentage of git users know what rebase does. In its simplest form, it takes one series of commits -- typically from a branch --, detaches them from their parent commit and glues them onto the tip of another parent commit (which is frequently just the updated tip of same branch).

I started writing this post about `rebase`, but it ended up being partly about the curious `git fetch origin <src>:<dest>` syntax -- the `<src>:<dest>` part is a [refspec](https://git-scm.com/docs/gitglossary#def_refspec). Read on for details.

This post will take you through:
- The concept of rebasing
- The 4 commands that most tutorials contain
- How to cut that down to 2 commands and eliminate branch switches
- What the odd-looking `git fetch origin <src>:<dest>` command does

### Example: rebasing (the long way)
**Note**: if you're familiar with rebase, skip on to the next bit.

We branched off `main` a while back (commit `m3` to be precise), but after fetching the latest version of `main`, we can see new commits were made: `[m4, m5]`. 
```
m1  m2  m3  m4  m5
o---o---o---o---o branch: main
         \
          a1  a2
          o---o branch: a
```

We want to update our branch `a` (with commits `[a1, a2]`) so that it's branched off the latest version of `main`, aka commit `m5`.

```
m1  m2  m3  m4  m5
o---o---o---o---o branch: main
                 \
                  a1' a2'
                  o---o branch: a
```
**Note**: The commits `[a1', a2']` (pronounced a1 prime, a2 prime) no longer have the same commit hashes, even if the underlying change content is identical -- a commit hash is calculated using the parent commit(s), message, file contents and more. The parent commit has changed, so the hash has too.

What commands do we need to execute to achieve this goal state? Most tutorials will tell you to run a series of commands similar to the following (assuming we've got branch `a` checked out and active):

```shell
# we're on branch `a`, so let's switch to the main branch
~/example (a) $ git switch main

# fetch latest changes and fast-forward the main branch
# this isn't the rebase we're interested in, though
~/example (main) $ git pull origin main --rebase

# switch back to last active branch, equiv. to `git switch a`
~/example (main) $ git switch -

# rebase, which basically says "glue branch a to the tip of main`
~/example (a) $ git rebase main
```

### A slicker way -- use `git fetch origin main:main`
If you're like 95% of GitHub/BitBucket/Whatever projects these days, developers directly commits to the `main` branch or push it (or whatever your trunk branch is called). Consequently, the `main` branch is effectively readonly. Our Continuous Integration (CI) processes handle the merges to `main`. 

This helps because we'll never be locally editing `main`, so all updates will be saying to git, "please make my version of `main` reflect the remote's version of things".

Since we no longer need to merge or resolve conflicts on `main`, we can use the following (slightly odd-looking) `git fetch` syntax to streamline things:
```shell
# again, we've got branch `a` checked out and active
~/example (a) $ git fetch origin main:main

# rebase our `a` branch against freshly updated `main`
~/example (a) $ git rebase main
```

"Bringo." We've halved the number of required commands. As there's no need to switch to `main`, there's no need to switch back to `a` -- we were never switched to `main` in the first place!

The slightly odd-looking `git fetch origin <src>:<dst>` [refspec](https://git-scm.com/docs/gitglossary#def_refspec) syntax fetches `main` from the remote and updates our local copy to match it. If your local `main` branch has commits not present on the remote, the command will be rejected so as to preserve your local repo's history.

If you're a devil-may-care type, you can overwrite your local history by prepending `+` to the start of the refspec:

```shell
# I wouldn't recommend doing this, as it can be destructive
~/example (a) $ git fetch origin +main:main
```

I've been carping on about `git rebase`, but we can use the same `git fetch` trick even if we're going to use `git merge` to fold the latest `main` contents into `a`, instead. I just so happen to prefer rebasing by default:

```shell
# again, we've got branch `a` checked out and active
~/example (a) $ git fetch origin main:main

# merge the latest main into `a`
~/example (a) $ git merge main
```

So there we go. You can now rebase or merge faster and while using fewer commands. You also now understand what the funky refspec syntax does.

**Note**: This blog post was hand-written -- I am not a robot 🤖🔫.
