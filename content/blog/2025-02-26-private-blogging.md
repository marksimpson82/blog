+++
title = "Private Blogging (a.k.a. why this blog is a barren wasteland)"
tags = ["blogging", "obsidian", "note-taking"]
+++

## Q: How do you take notes? A: Privately.
As a follow-on from [How do you take notes?](@/blog/2022-10-30-obsidian.md), I thought I'd write a (very) short update.

tl;dr: I've been using Obsidian for my personal note-taking since 2022, and I really like it.
- I have a private git repository
- I write my notes in markdown (just like this blog)
- I don't have to care about whether the subject I'm writing about is boring or suitable for sharing (like this!)
- I am free to mix plain text with code snippets, or reference (small) files, whatever
  - This is especially useful for things I've partly automated and use infrequently
- I can come back to things I'd often forget, e.g. boiler part numbers / instructions

## Downsides
The downside is that it's temporarily killed this blog. 

It may look like I'm in a coma, but I am still furiously writing. The posts are not shared, though. When I have to tackle a subject, I tend to just write my own notes to clarify my own thoughts, e.g. in no particular order:
- Git spells and internals
- Testing microservices
- The boundaries of various testing / faking approaches
  - In process
  - Out of process
  - Using tools like Wireshark
- Learning golang
- Learning AI/LLM fundamentals (I won't subject anyone to this, plenty of awesome resources out there!)

## Public blogging
I've had to fix my public blog a few times because the GitHub action that publishes broke a few times. It's now back up.

I will try and cherry pick a few interesting topics and re-shape a few for my public blog.

Here's a sample of what I've been writing about but not sharing.
```bash
# print total line count for markdown files; 
# show the largest by line count in desc. order
$ find . -name '*.md' | xargs wc -l | sort -nr
 17446 total
   # I've got a few git presentations in me at this point
   774 ./it_and_software/software_engineering/git_internals.md
   349 ./it_and_software/software_engineering/git_spells.md
      
   # Open Media Vault / Jellyfin install steps / config 📼
   332 ./it_and_software/install_omv.md
   
   # Andrej Karpathy's videos are great primers / explainers
   # on modern LLMs, recommended! 🤖
   330 ./it_and_software/software_engineering/ai/ai_karpathy_001_llm_overview.md
   
   # Is it a data lake? No! It's a data lake ... house, of course 🤦‍♂️
   319 ./data/data_lakehouse.md
   
   # Had to use 🥒. Do not like ❌. It has its place, but customers
   # and non-engineers often want it, but then don't contribute
   # so you have extra complexity to carry for little gain
   301 ./it_and_software/testing/cucumber_gherkin.md

   # Data testing with great expectations 👩‍💻🧪. 
   # Works OK with batch, but if upstream data is bad... welp
   284 ./data/testing/great_expectations/ge_approaches.md

   # Microservice 'component' testing. Check out:
   # - Martin Fowler's stuff
   # - Cindy Sridharan's 'step up rule', too.
   # https://copyconstruct.medium.com/testing-microservices-the-sane-way-9bb31d158c16
   262 ./it_and_software/testing/microservice_testing.md 
   
   # Had to write one at 🔫👈, but then nobody reads it 😭
   # Cleaned up a few templates for future projects
   250 ./it_and_software/testing/qa_test_strategy.md
   201 ./it_and_software/testing/qa_test_plan.md
   
   # hx is an alternative to vi/vim/neovim. Works well.
   # I wouldn't bother switching if you know vi/vim, though
   235 ./it_and_software/helix_editor.md

   # go's out of the box testing is good,
   # but the boilerplate can be irritating
   234 ./it_and_software/testing/go_testing.md

   # won't it ever be the year of linux desktop? 
   # Give me 100% modern gaming on Linux and I'm gone 🏃‍♂️💨
   233 ./it_and_software/install_windows10.md

   # won't it ever be the year of heat pumps in old UK flats, ffs? 
   # Heat Geeks for 🧠🎓 though! https://www.heatgeek.com/
   223 ./home_and_diy/boiler_replacement.md
 
   # playwright is great for headless browser testing & automation
   183 ./it_and_software/testing/playwright.md

   # my .gitconfig and spells 👩‍💻
   172 ./it_and_software/software_engineering/git_config.md

   # etc   
```

... and so on.