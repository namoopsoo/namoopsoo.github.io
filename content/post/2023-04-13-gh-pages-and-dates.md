---
date: 2023-04-13
title: Run forever!
---

### Github Pages build queued for a day 
```
 "Waiting for a runner to pick up this job"
```

#### But I was excited to release a date fix
The dates on hugo posts were funky since switching to PaperMod, like "121212-34-7878"

But I was reading newer hugo uses `date_format` instead of `dateFormat`. 

Anyway I had a typo because I had `DateFormat` , would not have worked anyway. 

But I could not publish this! 

#### Oh ubuntu-18- no longer supported 
So per [stacko](https://stackoverflow.com/questions/70959954/error-waiting-for-a-runner-to-pick-up-this-job-using-github-actions), I switched from 
```
runs-on: ubuntu-18.04 
```
to
```
runs-on: ubuntu-latest
```
because https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources

#### Dates displaying normally now haha
Nice 
