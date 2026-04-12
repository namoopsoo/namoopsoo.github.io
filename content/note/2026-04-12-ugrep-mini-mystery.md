---
date: 2026-04-12
title: No, you grep !
---

I recently<sup>[1](#references)</sup> discovered `ugrep`, and I have benefited a lot in using this to search my logseq journals. But recently I noticed I was getting less results and also confirmed some misses. My specific strange issue was that if I pointed directly to my miss, `ug` found it but not otherwise. I was consulting with microsoft copilot about this mystery. 

> running into a weird ugrep issue where, `ug -%% 'some blah' /some/foo/path` , comes up dry , but if I am specific `ug -%% 'some blah' /some/foo/path/more/specific/file.py` , then I get results. Is there some index that needs to be poked for rebuilding?

  
Insights included turning on `--hidden` and `--all` , to search in `.gitignore` and other hidden files, as well as following symlinks. Those did not work for me. I went through a few more back and forths in the conversation but nope nothing. One cool suggestion was to use `--stats`. This was helpful because `ug` will report how many directories and files were searched and when I tried this I  saw way fewer directories than expected. And then the answer was obvious 🤦‍♂️,  `ug` was likely not looking recursively. My original success was on my logseq journal which is just a flat directory and so I did not encounter this issue.

## My session

{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/there some index that needs to be poked for rebuilding.jpeg" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/2026-04-12_1358--0400.jpeg" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/Directory search faring while file search works almost always means.jpeg" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/sofetyUX defautts that stop directory walks early or slip content. You can get past all of them, selectively or.jpeg" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/The Nuclear Option (fully unbounded search).jpeg" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/are just simple normal fies, but ug does not find them..jpeg" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/How to force deeper traversal.jpeg" width="50%">}}

I am logging this as another example where GPT on copilot was not seeing the obvious answer. It took me a while to grok this but in my defense I had a solid 30 days of benefit where I just so happened to only use this on a flat directory 😆. 

### Chat GPT got it out of the box
However, I also tried Chat GPT, and there I got the right answer right away actually.

{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/Pasted Graphic.png" width="50%">}}

### Copilot got it with deep thinking selected

{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/Recommended practical alias.jpeg" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-04-12-ugrep-mini-mystery/2026-04-12_1358--0400.jpeg" width="50%">}}


# References
1. https://michal.piekarczyk.xyz/note/2026-03-01-immich-video-update/#ugrep-ug

