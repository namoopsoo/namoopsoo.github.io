---
date: 2025-04-05
title: collect logseq logbook stats
---

Figured, I'm not good at logseq datalog queries yet, so may as well just read logseq LOGBOOK data using plain python.

And with assist of chat gpt, I have a nice proof of concept.

```python
from pathlib import Path
import polars as pl
import time_log as tl

journals_dir = "mgraphblah/journals"
pattern = "2025_*.md"
out_vec = tl.iterate_across_journals(journals_dir, pattern)
df = pl.from_dicts(out_vec)
```

how much time I spent on taxes?
```python
per_tag_stats = df.explode("Tags").group_by("Tags").agg(pl.col("Duration (mins)").sum().alias("Total minutes"))
per_tag_stats.filter(pl.col("Tags") == "my taxes/2024")

```
```
┌───────────────┬───────────────┐
│ Tags          ┆ Total minutes │
│ ---           ┆ ---           │
│ str           ┆ i64           │
╞═══════════════╪═══════════════╡
│ my taxes/2024 ┆ 260           │
└───────────────┴───────────────┘
```


# Source
time_log.py

```python
import re
import csv
import argparse
from datetime import datetime
from pathlib import Path
import polars as pl



def parse_clock_line(line):
    pattern = r"CLOCK: \[(.*?)\]--\[(.*?)\]"
    match = re.search(pattern, line)
    if match:
        start_str, end_str = match.groups()
        start_dt = datetime.strptime(start_str, "%Y-%m-%d %a %H:%M:%S")
        end_dt = datetime.strptime(end_str, "%Y-%m-%d %a %H:%M:%S")
        duration = end_dt - start_dt
        return start_dt, end_dt, duration
    return None, None, None

def extract_time_blocks(filepath):
    rows = []
    with open(filepath, 'r', encoding='utf-8') as file:
        current_task = None
        for line in file:
            line = line.strip()
            if line.startswith('- '):
                current_task = line[2:]
            elif line.startswith('CLOCK:'):
                start_dt, end_dt, duration = parse_clock_line(line)
                if start_dt and end_dt:
                    rows.append({
                        'Date': start_dt.date(),
                        'Start': start_dt.time(),
                        'End': end_dt.time(),
                        'Duration (mins)': round(duration.total_seconds() / 60),
                        'Task': current_task,
                        'Tags': parse_tags_from_task(current_task),
                    })
    return rows

def parse_tags_from_task(task_line):
    if not task_line:
        return []

    tags = []

    # Match [[tag with spaces]]
    tags += re.findall(r"\[\[([^\]]+)\]\]", task_line)

    # Match #tag (without brackets)
    tags += re.findall(r"#([a-zA-Z0-9/_\-]+)", task_line)

    return tags

def iterate_across_journals(journals_dir, pattern):
    out_vec = []
    for input_md_file in Path(journals_dir).glob(pattern):
        ...
        parsed_rows = extract_time_blocks(input_md_file)

        out_vec.extend(parsed_rows)

    return out_vec

```
