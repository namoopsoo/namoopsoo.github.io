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
    m = re.match(r"^(?P<title>.*)[(](?P<author>.*)[)]\n- Your (?P<type>Highlight|Note|Bookmark) on (page (?P<page>\d+) [|] )?Location (?P<location>\d+(-\d+)?) [|] Added on (?P<timestamp>.*)(\n\n)?(?P<content>.*)", entry)
    return m.groupdict()
```

##  References
1. https://github.com/prime-radiant-inc/kindle-highlight-exporter , https://highlights.primeradiant.com/
2. https://read.amazon.com/notebook
