---
title: "2026 06 14 Kindle Notes"
# slug: "2026-06-14-kindle-notes"
date: 2026-06-14T11:53:51-04:00
# draft: true

# optional thumbnail
images:
  - "THUMBNAIL_PLACEHOLDER"
cover:
  image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->



I tried out this<sup>[1](#references)</sup> cool tool for extracting amazon kindle notes. It is way better than emailing myself a pdf of notes like I had done in the past. Then I had some script I lost for converting from pdf to markdown. This project just pulls directly from amazon<sup>[2](#references)</sup>   which I didn't even know was a place your notes go! I used this bookmarklet tool from Prime Radiant Inc and pulled my notes, but then I tried looking at my kindle Clippings file directly also, which looks like is even easier.

However, when I compared my nearly 2 megabyte dump from read.amazon , with my `My Clippings.txt` at just under 1 megabyte, I realized, right, I have switched kindles in the past and so the 2 megabyte one has more notes. I found 18 books in my clippings and 57 in my historical file. So that sort of adds up.

## clippings directly 
Counted unique books from notes
```python
import re
from pathlib import Path
clippings = Path("/Volumes/Kindle/documents/My Clippings.txt").read_text()
notes = clippings.split("==========")
def extract_book(s):
    m = re.match(r"^(.*)[(]", s.strip().strip("\ufeff"))
    if m:
        return m.groups()[0].strip()

books = [extract_book(x) for x in notes if extract_book(x) is not None]
len(notes), len(books), len(set(books))
```

notes structured 
```python

def extract_entry(s):
    entry = s.strip().strip("\ufeff")
    m = re.match(r"^(?P<title>.*)[(](?P<author>.*)[)]\n- Your (?P<type>Highlight|Note|Bookmark) on (page (?P<page>[\dlvixcd]+) [|] )?Location (?P<location>\d+(-\d+)?) [|] Added on (?P<timestamp>[^\n]+)(\n\n)?(?P<content>.*)", entry, re.DOTALL)
    return m.groupdict() if m else {"raw": entry}
```
Kind of a funny side note haha my regex above was failing for some of my notes, in particular like, 
```
Meditations (Modern Library) (Aurelius, Marcus)
- Your Highlight on page xlviii | Location 632-635 | Added on Thursday, November 27, 2025 8:48:32 PM

elaborate scene setting that we expect in a true dialogue, but we do find in a number of entries a kind of internal debate in which the questions or objections of an imaginary interlocutor are answered by a second, calmer voice which corrects or rebukes its errors. The first voice seems to represent Marcus’s weaker, human side; the second is the voice of philosophy.

```
so I thought ahh ok the title can also have a parenthesis, "Meditations (Modern Library)", but no haha that was not the problem in my regex. The problem was my page regex, `(?P<page>\d+)` did not capture roman numerals. Of course the only uncaptured notes in my kindle notes with roman numeral pages were for a Roman author 😂.
 
Okay I burned about an hour and twenty minutes on the above regex to extract my notes from my kindle clippings. Yes I could have either downloaded a package, or used Chat GPT to cook up the regex, but then I wouldn't have had that funny Roman author Roman numerals anecdote!

##  References
1. https://github.com/prime-radiant-inc/kindle-highlight-exporter , https://highlights.primeradiant.com/
2. https://read.amazon.com/notebook
