---
title: Chopin Etude op 10 no 1 progress with voice memo and ffprobe and chatgpt
date: 2025-02-22
---

I've been recording my progress on Chopin Etude op 10 no 1, for a few years now and figured I'd see where I'm at now. 

Asked chatgpt for help. I've been recording to `.m4a` by mac voice memo. I just downloaded my files. I had been using a more or less consistent file naming. Chatgpt generated a quick script for `polars` ( because I had stopped using `pandas` about a year ago ).


And of course for the record I'm aware this in no way reflects mistakes or how well this sounds but only speed. Apparently there is some super interesting research being done on quality too. (Not sure if it is available to the mainstream yet but see a cool blogpost here https://www.launchpad.ai/blog/an-ai-based-method-for-student-piano-performance-assessment ).


In any case for speed, here is what I have. This assumes `ffprobe` is available, which comes with `brew install ffmpeg`.

```python
from pathlib import Path
workdir = Path().home() / "Dropbox/AudioRecordings/piano"
import polars as pl

durations = process_audio_files(workdir)

durations[:4]
```
```python
# Out[6]: 
[{'filename': '2019-10-15-Chopin-etude-op10-no2.m4a', 'duration': '06:25'},
 {'filename': '2023-02-19-chopin-etude-op-10-no-1.m4a', 'duration': '05:13'},
 {'filename': '2020-11-02-Chopin-op10-etude1.m4a', 'duration': '06:41'},
 {'filename': '2019-10-26-Chopin-etude-op10-no2.m4a', 'duration': '05:42'}]

```
```python
df = pl.from_dicts(durations)

df.filter(pl.col("filename").str.contains("op-10-no-1")).sort(by="duration")
```
```
# Out[13]: 
shape: (27, 2)
┌─────────────────────────────────┬──────────┐
│ filename                        ┆ duration │
│ ---                             ┆ ---      │
│ str                             ┆ str      │
╞═════════════════════════════════╪══════════╡
│ 2023-02-19-chopin-etude-op-10-… ┆ 05:13    │
│ 2023-02-14-chopin-etude-op-10-… ┆ 05:34    │
│ 2023-10-14-Chopin-etude-op-10-… ┆ 05:45    │
│ 2021-04-17-23.08-Chopin-Étude…  ┆ 05:53    │
│ 2025-02-22-Chopin-etude-op-10-… ┆ 05:56    │
│ …                               ┆ …        │
│ 2020-08-05-Chopin-etude-op-10-… ┆ 09:05    │
│ 2020-05-30-T1214-Chopin-etude-… ┆ 09:19    │
│ 2020-09-08-Chopin-etude-op-10-… ┆ 09:23    │
│ 2020-06-23-Chopin-etude-op-10-… ┆ 09:29    │
│ 2020-05-30-Chopin-etude-op-10-… ┆ 10:04    │
└─────────────────────────────────┴──────────┘

```

```python
with pl.Config(tbl_rows=40):
    print(df.filter(pl.col("filename").str.contains("op-10-no-1")).sort(by="duration"))
```
```python
shape: (27, 2)
┌─────────────────────────────────┬──────────┐
│ filename                        ┆ duration │
│ ---                             ┆ ---      │
│ str                             ┆ str      │
╞═════════════════════════════════╪══════════╡
│ 2023-02-19-chopin-etude-op-10-… ┆ 05:13    │
│ 2023-02-14-chopin-etude-op-10-… ┆ 05:34    │
│ 2023-10-14-Chopin-etude-op-10-… ┆ 05:45    │
│ 2021-04-17-23.08-Chopin-Étude…  ┆ 05:53    │
│ 2025-02-22-Chopin-etude-op-10-… ┆ 05:56    │
│ 2021-05-22-Chopin-etude-op-10-… ┆ 05:59    │
│ 2021-02-28-Chopin-etude-op-10-… ┆ 06:06    │
│ 2023-07-01-Chopin-etude-op-10-… ┆ 06:20    │
│ 2020-12-22-Chopin-etude-op-10-… ┆ 06:31    │
│ 2021-03-06-Chopin-etude-op-10-… ┆ 06:37    │
│ 2020-11-02-Chopin-etude-op-10-… ┆ 06:41    │
│ 2021-01-22-Chopin-etude-op-10-… ┆ 06:54    │
│ 2020-11-09-Chopin-etude-op-10-… ┆ 07:00    │
│ 2020-11-29-Chopin-etude-op-10-… ┆ 07:00    │
│ 2020-12-20-Chopin-etude-op-10-… ┆ 07:33    │
│ 2020-10-29-Chopin-etude-op-10-… ┆ 07:37    │
│ 2020-09-27-Chopin-etude-op-10-… ┆ 07:50    │
│ 2020-08-26-Chopin-etude-op-10-… ┆ 07:56    │
│ 2020-10-11-chopin-etude-op-10-… ┆ 08:02    │
│ 2020-12-27-Chopin-etude-op-10-… ┆ 08:12    │
│ 2020-07-12-Chopin-etude-op-10-… ┆ 08:29    │
│ 2020-06-10-chopin-etude-op-10-… ┆ 08:38    │
│ 2020-08-05-Chopin-etude-op-10-… ┆ 09:05    │
│ 2020-05-30-T1214-Chopin-etude-… ┆ 09:19    │
│ 2020-09-08-Chopin-etude-op-10-… ┆ 09:23    │
│ 2020-06-23-Chopin-etude-op-10-… ┆ 09:29    │
│ 2020-05-30-Chopin-etude-op-10-… ┆ 10:04    │
└─────────────────────────────────┴──────────┘

```

### for reference here is the script

```python
import subprocess
import os

def get_audio_duration(file_path):
    """Gets the duration of an audio file using ffprobe."""
    if os.path.getsize(file_path) == 0:
        return "00:00"  # Handle empty files gracefully

    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duration = float(result.stdout.strip())
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return f"{minutes:02}:{seconds:02}"
    except Exception as e:
        return f"Error: {e}"

def process_audio_files(folder_path):
    """Processes all M4A files in a given folder and returns their durations."""
    audio_files = [f for f in os.listdir(folder_path) if f.endswith(".m4a")]
    audio_durations = []

    for file in audio_files:
        file_path = os.path.join(folder_path, file)
        
        if os.path.getsize(file_path) == 0:
            duration = "00:00"  # Skip empty files
        else:
            duration = get_audio_duration(file_path)
        
        audio_durations.append({"filename": file, "duration": duration})

    return audio_durations


```


