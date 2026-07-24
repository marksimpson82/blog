---
title: "git-rebase-onto"
date: 2026-07-25T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - git
  - rebase
  - vcs
  - scm
---

## git rebase --onto
If you're not familiar with `git rebase`, I wrote a bit of a primer in [a previous post about basic rebasing and git fetch tricks]({% post_url 2026-07-24-git-rebase-trick-fewer-commands %}), so it might be worth reading that first.

The rest of this post is for git users who're comfortable with basic rebasing. I'm going to explain how to use `git rebase --onto`, the problem it solves and why you might find it useful. 

**Warning**: As ever, rebase-based workflows are intended for branches with only a single contributor. If multiple developers are pushing to the same branch, I wouldn't recommend rebasing it.

### What does the `--onto` option do?
While the [documentation](https://git-scm.com/docs/git-rebase#_options) is fairly dry, there is a [worked example](https://git-scm.com/docs/git-rebase#_transplanting_a_topic_branch_with_onto) that's more illuminating, too.

Docs aside, what do _I_ use `--onto` for? I use it when I have 'stacked' branches and Pull Requests (PRs). I like to create easily reviewable, self-contained commits and PRs. Also, for the purposes of this post, we'll assume that the smallest mergeable unit is a PR.

The thing with creating small PRs is that, unfortunately this sometimes means branching off a branch. E.g. let's say we're implementing a feature and realise the code we're extending is a bit of a mess. While we could create a PR containing both the refactor and the feature addition, this causes problems:

1. It mixes non-functional (refactoring) and functional (feature work) changes
2. It increases the PR size
3. It makes the PR harder to read, understand and review

If we have a good idea of what's to be done, we could structure our changes such that we have `main <- refactor <- feature`, e.g.:

```
m1  m2  m3
o---o---o branch: main
         \
          r1  r2
          o---o branch: refactor
               \
                f1  f2
                o---o branch: feature               
```

**Aside**: There are multiple ways to structure this. You don't even necessarily need multiple local branches, but that's for another day :-)

These PRs are smaller and easier to review. The downside is that there's more dependencies involved, and landing those PRs back into `main` requires extra care.

### How do we land dependent PRs into main?
In the above example with `refactor` and `feature` PRs, the latter builds on the former, so we need to get our `refactor` branch's changes into `main` as the first step. 

Firstly, let's merge `refactor` into `main` using a squash commit. If we're using GitHub, BitBucket or any other forge that uses PR flows, we use the UI or CLI to merge the `refactor` branch into `main`, then pull `main`.

If we're using plain ol' git and no forge, we can run the commands:

```shell
git switch main
git merge --squash refactor
git commit
```

After the first squash merge, our local repo will look like this, as the content from the `refactor` branch's commits `[r1, r2]` is now in commit `m4`:

```
m1  m2  m3  m4 (squash: r1 + r2)
o---o---o---o branch: main
         \
          r1  r2
          o---o branch: refactor
               \
                f1  f2
                o---o branch: feature               
```

So `refactor`'s contents are in `main`.  We're halfway there. Unfortunately, we've got a few problems:
1. The `refactor` branch is stale and just kinda existing despite its contents existing in `main` via our squash merge
2. Our `feature` branch is still connected to the tip of `refactor`

Before we can merge `feature` into `main`, we need to rebase it. Instead of `f1`'s parent being `r2`, we need to re-parent it to `m4` (remember, `m4` contains the contents of `[r1, r2]`).

### Let's use `git rebase --onto`
The documentation for `git rebase --onto` isn't the easiest to follow, but the usual use case isn't too hard to remember once you try it a few times.

```shell
git rebase --onto <new-base> <old-base> <branch-to-move>
```

- `<new-base>`: The new starting point for our commits
- `<old-base>`: The old starting point -- this basically tells `git`, "don't take any commits before this one"
- `<branch-to-move>`: The branch we're rebasing

In our example, run the following to get the desired effect:

```shell
git rebase --onto main refactor feature
```

This tells git rebase:
- The commit we want as our new parent is the tip of the `main` branch
- The old parent commit is the tip of the `refactor` branch (this effectively excludes the branch's commits from the rebase operation)
- The commit we want to rebase up to is the tip of `feature`

After running the command, we get the following structure:

```
m1  m2  m3  m4 (squash: r1 + r2)
o---o---o---o branch: main
             \
              f1  f2
              o---o branch: feature               
```

You can now push the updated `feature` branch to the remote via:

```shell
git push origin feature --force-with-lease
```

**Note**: The old `refactor` branch still exists at this point; I omitted it from the diagram for brevity. You can delete it via your forge's controls and/or through git itself:

```shell
git branch -D refactor
git push origin --delete refactor
```

### References
I found GitHub dev [sameenkarim's comment on HN](https://news.ycombinator.com/item?id=47759587) really useful for understanding how this all worked.

```
Yes, we handle this both in the CLI and server using git rebase --onto

  git rebase --onto <new_commit_sha_generated_by_squash> <original_commit_sha_from_tip_of_merged_branch> <branch_name>

So for ex in this scenario:

  PR1: main <- A, B              (branch1)
  PR2: main <- A, B, C, D        (branch2)
  PR3: main <- A, B, C, D, E, F  (branch3)

When PR 1 and 2 are squash merged, main now looks like:

  S1 (squash of A+B), S2 (squash of C+D)

Then we run the following:

  git rebase --onto S2 D branch3

Which rewrites branch3 to:

  S1, S2, E, F

This operation moves the unique commits from the unmerged branch and replays them on top of the newly squashed commits on the base branch, avoiding any merge conflicts.
```

**Next time:** This reminds me that I should also write about why squash "merges" are not actually merge commits (they have one parent, a merge commit by definition must have two or more parents), and how forges retain context and links to long-merged PRs despite this lack of linkage in the git commit history.

**Note**: This blog post was hand-written -- I am not a robot 🤖🔫.