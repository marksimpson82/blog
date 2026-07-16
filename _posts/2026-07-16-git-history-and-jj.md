---
title: "The new git history commands"
date: 2026-07-16T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - git
  - history
  - jj
---

**Note**: This blog post was hand-written -- I am not a robot 🤖🔫.

## git has some rough edges
Git has been around a long time (I've been using it since around 2011, where'd the time go?) and doesn't seem to be going anywhere. The main advantage with git is the flexibility -- if you can think of doing something, you probably _can_ do it. The downside is that its cli commands often lack comfort and consistency (and I'm saying that as someone who has a good grasp of its internals and is often the friendly "please help me fix my git disaster" guy).

Sometimes fairly simple things require incantations and a small sacrifice. I'm not sure if "un-ergonomic" is the right term, but git certainly can be trying -- there's a reason https://ohshitgit.com/ is a thing. I occasionally still backup branches before I perform git surgery. Still, it beats using Perforce, SVN or CVS.

## Problem: `git checkout`
Even everyday commands can be unwieldy. Here's an example of a particularly old, overloaded command: [`git checkout`](https://git-scm.com/docs/git-checkout).

```
git checkout [-q] [-f] [-m] [<branch>]
git checkout [-q] [-f] [-m] --detach [<branch>]
git checkout [-q] [-f] [-m] [--detach] <commit>
git checkout [-q] [-f] [-m] [[-b|-B|--orphan] <new-branch>] [<start-point>]
git checkout <tree-ish> [--] <pathspec>…​
git checkout <tree-ish> --pathspec-from-file=<file> [--pathspec-file-nul]
git checkout [-f|--ours|--theirs|-m|--conflict=<style>] [--] <pathspec>…​
git checkout [-f|--ours|--theirs|-m|--conflict=<style>] --pathspec-from-file=<file> [--pathspec-file-nul]
git checkout (-p|--patch) [<tree-ish>] [--] [<pathspec>…​]
```

If you're anything like me, you sort of internalised the cruftiness and forgot that one command does so much. `git checkout` can switch branches, swap to a [treeish object](https://git-scm.com/docs/gitglossary#def_tree-ish) (which itself can point to a [commitish](https://git-scm.com/docs/gitglossary#def_commit-ish) object!) and also restore working tree files. The same command that swaps branches also undoes your edits on a pathspec. 

I remember someone getting confused as to why their new CI script worked, because they accidentally passed a tag instead of a branch name. `git checkout` will happily work with either...

## Solution: `git switch` and `git restore`
The good news is that the maintainers have been slowly chipping away at this weakness. I've noticed several quality of life changes over the years, including for the aforementioned problems with `git commit`:
- `git switch [-c] <name>` for changing branches
- `git restore` for restoring working tree files

Anyway, that's just a small example of git's irritations and the things the devs are doing to improve matters. Let's get on to the main topic: rebasing.

## Problem: `git rebase`
Rebasing is a powerful and flexible command, but a lot of the things we do with `git rebase` are totally mundane. Unfortunately, everyday operations come with extra steps and friction.

Let's have a look at my git repo's history:
```shell
git log --oneline

d9aaeea (main) Bump concurrent-ruby from 1.3.6 to 1.3.7 (#26)
c4c0a27 Bump faraday from 2.14.2 to 2.14.3 (#27)
b5b03ce Bump faraday from 2.14.1 to 2.14.2 (#25)
1660b81 jellyfin database repair
fbeef58 (origin/main) Use `main` instead of `master` branch
```

Let's imagine I've not yet pushed the top 4 commits, and I want to edit commit `1660b81`. With `git rebase`, I'd have do one of the following:

**Option A: Create a fixup commit**
```shell
# make changes to working copy
git add -p blah.md
git commit --fixup 1650b81

# rebase to squash contents of our new fixup commit into the old one
git rebase -i --autosquash 1650b81^
```

**Option B: Edit the commit itself**
```shell
# stash our changes to blah.md
git stash

# rebase to pick the commit for editing. You might also want to throw in
# a cheeky --update-refs to force dependent branches to rebase, too
# but this is already complicated enough
git rebase -i 1660b81^
```

Then select commit 1660b81 for editing in the interactive rebase menu:

```
# git opens a text editor with a list of commits to manipulate
pick d9aaeea # Bump concurrent-ruby from 1.3.6 to 1.3.7 (#26)
pick c4c0a27 # Bump faraday from 2.14.2 to 2.14.3 (#27)
pick b5b03ce # Bump faraday from 2.14.1 to 2.14.2 (#25)
edit 1660b81 # jellyfin database repair
pick fbeef58 # Use `main` instead of `master` branch
```

Then a load more annoying steps:
- Unstash the stashed edits with `git stash apply` or `pop`
- Stage them via `git add`
- Commit them via `git commit`
- Resume the `rebase` via `git rebase --continue`

## Solution: `git history`
[Git v2.54.0](https://gitlab.com/git-scm/git/-/blob/HEAD/Documentation/RelNotes/2.54.0.adoc) quietly introduced a new `git history` command:
> "git history" history rewriting (experimental) command has been added.

[Git v2.55.0](https://gitlab.com/git-scm/git/-/blob/HEAD/Documentation/RelNotes/2.55.0.adoc) went one further, extending it with the `fixup` subcommand:
> "git history" learned "fixup" command.

Let's edit our commit using `git history fixup`:

```shell
# we're on d9aaeea -- the tip of main
git add -p blah.md
git history fixup 1660b81
```

And we're done. With these two commands we've done the following:
- Squashed the staged changes to `blah.md` into the commit `1660b81`
- Rebased the rest of the branch's changes relative to the edit
- Rebased any dependent branches, too (similar to `git rebase --update-refs`, I think?)

In addition to `git history fixup`, you can also use `git history reword` to rewrite the commit message _without_ faffing about with the interactive rebase process. It's so much nicer.

Finally, there's `git history split <commit> [--] [<pathspec>]` which is a little more complicated. It takes a commit hash plus an optional pathspec, then opens an interactive session that functions similarly to patch mode (`git add -p`). Any hunks that you stage will be moved into a new parent commit of the one chosen by the command.

E.g. let's say we made a commit that contained a mixture of documentation changes and code changes. We want to split the docs into a new parent commit.

```shell
# select all the .md files in the existing commit, this will open a session asking you to choose the hunks to move to a new commit
git history split 1660b81 -- '*.md'

# accept the .md changes via choosing y/n and we're done!
```

## An old dog learning new tricks?
Git is taking a leaf out of [`jj` aka `jujutsu`](https://docs.jj-vcs.dev/latest/)'s book by upgrading its history editing ergonomics. This is a positive for users regardless of which tool 'wins'.

 **Aside**: I've been playing with `jj` at home, and I'm quietly impressed. I'll write more on that shortly.
