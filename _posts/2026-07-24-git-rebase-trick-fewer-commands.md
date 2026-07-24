---
title: "git rebase trick -- fetch origin branch:branch"
date: 2026-07-24T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - git
  - rebase
  - vcs
  - scm
---
**Note**: This blog post was hand-written -- I am not a robot 🤖🔫.

## Git rebase basics
A decent percentage of git users know what rebase does. In its simplest form, it takes one series of commits -- typically from a branch --, detaches them from their parent commit and glues them onto the tip of another parent commit (which is frequently just the updated tip of same branch).

### Example: rebasing a branch `a` against the latest version of `main`
We branched off `main` a while back (commit `m3` to be precise), but after fetching the latest version of `main`, we can see new commits were made: `[m4, m5]`. 
```
m1  m2  m3  m4  m5
-o---o---o---o---o branch: main
         \
          a1  a2
          o---o branch: a
```

We want to update our branch `a` (with commits `[a1, a2]`) so that it's branched off the latest version of `main`, aka commit `m5`.

```
m1  m2  m3  m4  m5
-o---o---o---o---o branch: main
                  \
                   a1' a2'
                   o---o branch: a
```
**Note**: The commits `[a1', a2']` (pronounced a1 prime, a2 prime) no longer have the same commit hashes, even if the underlying change content is identical -- a commit hash is calculated using the parent commit(s), message, file contents and more. The parent commit has changed, so the hash has too.

What commands do we need to execute to achieve this goal state? Most tutorials will tell you to run a series of commands similar to the following (assuming we've got branch `a` checked out and active):

```shell
# we're on branch `a`, so let's switch to the main branch
git switch main

# fetch latest changes and rebase/fast-forward the main branch
# this isn't the rebase we're interested in, though
git pull # optionally add [--rebase] depending on workflow

# switch back to last active branch, equiv. to `git switch a`
git switch -

# rebase, which basically says "glue branch a to the tip of main`
git rebase main
```

### A slicker way -- use `git fetch origin main:main`
If you're like 95% of GitHub/BitBucket/Whatever projects these days, developers don't make commits or pushes to the `main` branch (or whatever your trunk branch is called). Consequently, the `main` branch is effectively readonly. Our Continuous Integration (CI) processes handle the merges to `main`. 

This helps because we'll never be locally editing `main`, so all updates will be saying to git, "please make my version of `main` reflect the remote's version of things".

Since we no longer need to merge or resolve conflicts on `main`, we can use the following (slightly odd-looking) `git fetch` syntax to streamline things:
```shell
# again, we've got branch `a` checked out and active
git fetch origin main:main

# rebase our `a` branch against freshly updated `main`
git rebase main
```

"Bringo." We've halved the number of required commands. As there's no need to switch to `main`, there's no need to switch back to `a` -- we were never switched to `main` in the first place!

The slightly odd-looking `git fetch origin <src>:<dst>` [refspec](https://git-scm.com/docs/gitglossary#def_refspec) syntax fetches `main` from the remote and updates our local copy to match it. If your local `main` branch has commits not present on the remote, the command will be rejected so as to preserve your local repo's history.

If you're a devil-may-care type, you can overwrite your local history by prepending `+` to the start of the refspec:

```shell
# I wouldn't recommend doing this, as it can be destructive
git fetch origin +main:main
```
