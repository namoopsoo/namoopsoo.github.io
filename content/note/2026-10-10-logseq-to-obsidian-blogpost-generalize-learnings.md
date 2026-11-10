---
type: my-blogpost
title: Generalize some logseq to obsidian migration learnings
date: 2026-10-10
---

Generalizing  some of the steps, I took, when migrating my logseq markdown for obsidian.

Two main steps here were just about the fact that logseq treats `#foo-tag` , `[[foo-tag]]` , and `#[[foo-tag]]` interchangeably, but i wanted to take advantage of Obsidian's use of tagging, so I wanted to convert all of my cases to just the square bracketed nodes. 

## tags to nodes

### First ran this sed script , for the simpler bracketed tags like `#[[foo node]]`

```sh
find pages journals -type f -name '*.md' \
  -exec sed -i.bak 's/#\[\[/[[/g' {} +
```

### and for the unbracketed tags, used python

this took 37 minutes on my markdown files 

```python
from pathlib import Path
import re
import time
from tqdm import tqdm

root = Path("/path/to/my-graph")

write_changes = True  # Change to True after reviewing the preview.

pattern = re.compile(
    r"""(?<!\S)#([\w/-]+(?:\.[\w/-]+)*)(?=[,;.!?'":]*(?:\s|$))"""
)

for folder in tqdm( ("pages", "journals") ):
    for path in tqdm(sorted((root / folder).rglob("*.md")), leave=False):
        time.sleep(1)
        # Preserve existing newline characters.
        with path.open("r", encoding="utf-8", newline="") as f:
            original = f.read()

        converted, count = pattern.subn(r"[[\1]]", original)
        if not count:
            continue

        # print(f"{path.relative_to(root)}: {count} replacements")

        if write_changes:
            with path.open("w", encoding="utf-8", newline="") as f:
                f.write(converted)

```

## TODO other notes 
can add other notes later, 