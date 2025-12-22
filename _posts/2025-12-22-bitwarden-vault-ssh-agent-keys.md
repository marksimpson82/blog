---
title: "Protecting SSH keys with BitWarden"
date: 2025-12-22T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - bitwarden
  - ssh
  - security
---

## Lots of hacks of late, some commonality
I've been reading a fair number of post-mortems of late due to the number of `npm` supply chain hacks. The hackers often run [`post-install` scripts](https://docs.npmjs.com/cli/v8/using-npm/scripts) to harvest credentials from the victim's machine. That is: once you've been pwned, the hacker will iterate through a number of directories that commonly store sensitive credentials (e.g. `~/.aws`, `~/.ssh`, etc.)

## By default, SSH keys live on the filesystem
If you've ever set up a GitHub account or used ssh for anything, you'll probably be aware of the fact that, by default, both your public **and private** SSH keys are stored on the filesystem, unencrypted.

Yup, `ls ~/.ssh/` and you'll see what I mean.

## Can we do better?
Yes. We can store SSH keys in a password manager such as [BitWarden](https://bitwarden.com). BitWarden has its own ssh agent built into its Desktop App (while BitWarden also offers a CLI, I'm not sure it offers SSH key integration like the desktop app).

Once enabled, an attacker cannot trivially hoover up SSH files from our `~/.ssh` directory because they no longer live there, in the clear.

The only downside is that you must run BitWarden desktop to enable the ssh keys. It adds a little bit of friction for a bit more security; I think it's a reasonable tradeoff. If the BitWarden app is open but locked, using an SSH key will cause the app to flash.

If you're not running BitWarden or fail to unlock the vault, you'll see something like the following (which isn't very user-friendly):

```shell
# git auth error example when BitWarden not running / unlocked
$ git pull
git@github.com: Permission denied (publickey).

# or something like
$ ssh-add -L
Could not open a connection to your authentication agent.
```

## Short version for Windows users
1. Follow the official [BitWarden tutorial steps](https://bitwarden.com/help/ssh-agent/)
1. However, it'll fail when trying to test the SSH agent via `ssh-add -L`
1. Skip ahead to the tutorial step that details how to change the `core.sshCommand`

It should then work. I've submitted feedback and a suggested fix to the page (on 2025-12-21), so hopefully they'll re-organise the steps. The `core.sshCommand` bit is currently tucked away under git commit signing, which is **not** needed to secure your SSH keys with BitWarden, hence why I think it should be moved earlier in the guide.

## Longer version
Again, this is for Windows. I don't think this affects Mac/Linux users.

The [BitWarden SSH documentation](https://bitwarden.com/help/ssh-agent/) has the instructions, but my opinion is the steps are a little out of order. Why? Because if you're using git bash on Windows, you absolutely **need** to set the following option regardless of whether you're signing git commits:

```shell
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
```

If you do not set this option, you'll receive an error message even when BitWarden is running and you've entered your master password to unlock the vault:

```
Could not open a connection to your authentication agent.
```

This is because the default `ssh` / `ssh-add` executables for git bash on Windows are different from the Windows defaults, and BitWarden is hooking into the OpenSSH versions, not the Git Bash ones.

Let's use a standard windows cmd prompt and see where our `ssh` / `ssh-add` binaries live:

```shell
# windows cmd -- you can see the OpenSSH binaries are first in $PATH
where ssh
C:\Windows\System32\OpenSSH\ssh.exe <- this is first in %PATH% and correct
C:\Program Files\Git\usr\bin\ssh.exe 

where ssh-add
C:\Windows\System32\OpenSSH\ssh-add.exe <- same
C:\Program Files\Git\usr\bin\ssh-add.exe

ssh-add -L  # succeeds
ssh-ed25519 ... etc

git pull  # succeeds as is using the expected ssh binaries
```

However, let's do the same thing using git bash or similar (e.g. I have a Windows Terminal config that launches `C:\Program Files\Git\bin\bash.exe`).

```shell
# git bash -- note: defaults to bundled git-provided ssh/ssh-add!
$ which ssh
/usr/bin/ssh  # really C:\Program Files\Git\usr\bin

$ which ssh-add
/usr/bin/ssh-add  # really C:\Program Files\Git\usr\bin

$ ssh-add -L  # fails because it's using the wrong ssh binary
Could not open a connection to your authentication agent.

$ git pull  # fails because using the wrong ssh binaries
```

Running the `git config` line above (or manually editing the `~/.gitconfig` setting) fixes the problem and tells git where to find the correct ssh binaries which play nice with BitWarden.

After making the config fix, I could run `ssh-add -L` and also `git pull/fetch/push` as expected.
