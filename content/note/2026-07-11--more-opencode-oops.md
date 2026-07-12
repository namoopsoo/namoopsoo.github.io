---
title: "More Opencode Oops"
# slug: "2026-07-11--more-opencode-oops"
date: 2026-07-11T15:25:39-04:00
# draft: true

# optional thumbnail
# images:
#   - "THUMBNAIL_PLACEHOLDER"
# cover:
#   image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->

I'm sure recommendations from a coding harness will vary in quality with the parameters of the model and the context available, but if these are not quite right, there will likely always be some room for error. 

Several interesting issues today with my semantic notes search project. I was using opencode with GPT 5.5 Fast recently and I ended up with pod memory monitoring that was not taking advantage of kubernetes capabilities and a parallelism split that did not align with my cluster node cardinality.

### Memory maxxing
I was having memory issues with my kubernetes job so I was using opencode to add memory logging. I ended up with the python `resource` module based monitoring. 

```python
import resource

def current_rss_mb() -> float | None:
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith("VmRSS:"):
            return int(line.split()[1]) / 1024

def max_rss_mb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
```
however I was realizing max rss or peak resident set size was not quite the actual total allocatable memory I was interested in, so I was doing some side research on Google, figuring maybe the kubernetes knowledge would be better there and indeed I learned about cgroups v2, where for modern kubernetes, two special files are available that answer my question, 

```python
CGROUP_MEMORY_CURRENT = Path("/sys/fs/cgroup/memory.current")
CGROUP_MEMORY_MAX = Path("/sys/fs/cgroup/memory.max")
```
This was more helpful in diagnosing some OOM issues.

### Bad parallelism
In another issue, I was setting up my kubernetes job yaml,  with opencode, but I ended up prompting for `parallelism=3` that was not proportional to my `number of nodes=2` and so my memory allocation of `2000MiB` per pod for my two `c6g.large` nodes of `3000MiB` didn't make sense since you can't split the `1000MiB` between two nodes for the third pod. This was a silly mistake on my part but haha the harness went along with my crazy request and that contributed to some of my memory issues. 😆.

### Erroneous automation
I was also using my harness to initially help me generate my job yaml and the original recommendation I got of running `kubectl apply -f job.yaml` was failing  with `InvalidImageName` because I edited the job yaml to use environmental variables  to keep my yaml free of secrets but they were taken as literals. Silly yes and after discussing this with opencode I got a cool recommendation to use `envsubst '$AWS_ACCOUNT_ID $AWS_REGION $DOCKER_TAG' < deploy/batch-embed.yaml | kubectl apply -f -`, to substitue with my env vars at runtime. But it was only after discussing the error I was getting. So this case is that my feedback was the additional context, but my yaml code was available to open code and the suggestion did not come up initially. So it is another example where I think trial and error is just the nature of the combinatorial work required for the universe we live in haha.

### Debugging memory issues
I'm collaborating with opencode and ChatGPT to troubleshoot why some of my kubernetes pods are getting OOMKilled. The EKS Auto Mode however kills my pods and their logs often before I get a chance to read them to see what happened. ChatGPT came up with a script to loop through my pods as they come online and tail them into a log. I kind of blindly trusted the script would work well because it was late in the evening, however in the morning I noticed the script runs into the same "pod not ready" issue I also often run into. So many of the logs just have 

```
Error from server (BadRequest): container "batch-embed" in pod "batch-embed-logseq-8-dwtq6" is waiting to start: ContainerCreating
```
I am reviewing the logs with opencode and I'm sure I'll get a workaround. However memory issues like this one are a category of problem where the frontier of possible troubleshooting approaches is  very wide and you often have to sample many of them to get anywhere. There is often a confluence of many different issues like unoptimized code, simple yaml configuration bugs and just parallelism/memory adjustments that require patient hand tuning.

### Patch bugs
And also ran into my kubernetes job erroring out with `NameError: name 'Path' is not defined` in the stack trace after a recent edit with my harness too. So after this I added `ruff check` as part of my `justfile` `just build`, to help spot bugs, introduced, well, either by me or by the harness. But still haha, this is more to my point about the iterative nature of edits, either by humans or by harnesses.

### Verifiability
That last example with linting with `ruff` is really the most telling, because I'm finding you can automate agentic programming more and more by having as much verifiability built in as possible. Currently I have been running opencode through its docker container like the below, but this is of course a bit limiting since the compact docker image does not include a python virtual environment with ruff or pytest

```
docker run -it --rm -p 1455:1455 -v ~/.local/share/opencode:/root/.local/share/opencode -v ~/.config/opencode:/root/.config/opencode -v "$PWD:/workspace" -w /workspace ghcr.io/anomalyco/opencode
```
However I should either add a virtual environment into this docker image or maybe I may consider something so bold as running it unencumbered!?

## A state space explosion
There are many problems that fit the out of memory kubernetes troubleshooting kind I described above. There is no one easy answer. There are may things you can try and each one branches into its own set of choices. Wicked problems hide around every corner in system challenges. Constraints help a lot. But I think agentic engineering is not a magic bullet to constraining that space, it's just that you can hopefully leverage agents to perhaps tackle more of it faster and more aggressively?!


## References
1. https://opencode.ai/
2. https://github.com/namoopsoo/logseq-semantic-search

