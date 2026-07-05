---
title: "Shard Spread Bug"
# slug: "2026-07-05--shard-spread-bug"
date: 2026-07-05T16:54:19-04:00
# draft: true

# optional thumbnail
#images:
#  - "THUMBNAIL_PLACEHOLDER"
#cover:
#  image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->
I have been pairing with codex to add parallelization to my logseq semantic search kubernetes batch job. Codex authored this function for checking if a shard environmental variable, `SHARD_INDEX`, should process a particular journal date among the set of journal dates to be processed. Paraphrasing the func, to just the basic hash algo, 

```python
def index_from_date(date_str, shard_count):
    digest = hashlib.sha256(date_str.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % shard_count
```
I wanted to test out of curiosity the distribution, and found it was wow pretty skewed, non uniform, 

```python
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict, Counter
  
shards = [index_from_date(
    (datetime(2026, 1, 1) + timedelta(days=i)).strftime("%Y_%m_%d"),
    shard_count=8)
    for i in range(365)
]

Counter(shards).most_common(8)
```
getting, 
```python
[(7, 64), (3, 52), (5, 51), (1, 43), (2, 42), (6, 41), (4, 40), (0, 32)]
```
I also started using open code today, attempting to check out if I can close the human in the loop gap in updates like this. So I asked GPT-5.5 fast through opencode, to fix this function to make it more uniform, otherwise my kubernetes nodes will be processing work quite asymmetrically. 

The updated code was to use the `date.toordinal()` instead which apparently is the number of days as of January 1st year 1. Very proleptically Georgian!
```python
def index_from_date(date_str, shard_count):
    date = date_from_str(date_str)
    return date.toordinal() % shard_count
```
 And opencode also added a test which it could not execute because the opencode docker container does not have python access somehow, but I ran the test and it ended up passing, checking that the `max(shards.values()) - min(shards.values())` spread  is less than or equal to 1. Worked out nicely.

checking manually also saw it was nice, 
```python
shard_count = 8
start = date(2026, 1, 1)
shards = Counter(
    shard_index_for_rel((start + timedelta(days=i)).strftime("%Y_%m_%d"), shard_count)
    for i in range(365)
)
shards.most_common(10)
```
getting, `[(1, 46), (2, 46), (3, 46), (4, 46), (5, 46), (6, 45), (7, 45), (0, 45)]`.


## Gut check 
So did I save time? Not sure yet haha. My document space is just files where the date `yyyy_mm_dd.md` is the path. What would I have done? Yea I would have also probably produced a day related number before passing it to the modulo `% 8`. And I would have tested it right away. So in this ecase I'm not sure if I saved time by outsourcing this code gen. But for sure I may have not had the thought to spot check the skew of this func and then I would have just had crappy asymmetric job spread and I would have noticed this later. So haha I will keep messing around with this of course. And I will keep trying to consider the net benefits. 

