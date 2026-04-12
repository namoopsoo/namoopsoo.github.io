---
date: 2026-04-12
title: you grep 
---

I recently<sup>[1](#references)</sup> discovered `ugrep`, and I have benefited a lot in using this to search my logseq journals. But recently I noticed I was getting less results and also confirmed some misses. My specific strange issue was that if I pointed directly to my miss, `ug` found it but not otherwise. I was consulting with microsoft copilot about this mystery. 

> running into a weird ugrep issue where, `ug -%% 'some blah' /some/foo/path` , comes up dry , but if I am specific `ug -%% 'some blah' /some/foo/path/more/specific/file.py` , then I get results. Is there some index that needs to be poked for rebuilding?

  
Insights included turning on `--hidden` and `--all` , to search in `.gitignore` and other hidden files, as well as following symlinks. Those did not work for me. I went through a few more back and forths in the conversation but nope nothing. One cool suggestion was to use `--stats`. This was helpful because `ug` will report how many directories and files were searched and when I tried this I  saw way fewer directories than expected. And then the answer was obvious 🤦‍♂️,  `ug` was likely not looking recursively. My original success was on my logseq journal which is just a flat directory and so I did not encounter this issue.

But I am logging this as yet another example where the latest GPT is not seeing the answer which is sort of the most obvious one. It took me a while to grok this but in my defense I had a solid 30 days of benefit where I just so happened to only use this on a flat directory 😆.

# References
1. https://michal.piekarczyk.xyz/note/2026-03-01-immich-video-update/#ugrep-ug

