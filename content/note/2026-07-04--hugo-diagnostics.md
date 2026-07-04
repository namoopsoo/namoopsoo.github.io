---
title: "Hugo Diagnostics"
# slug: "2026-07-04--hugo-diagnostics"
date: 2026-07-04T13:04:56-04:00
# draft: true

tags:
  - text-to-image

# optional thumbnail
images:
  - "https://s3.amazonaws.com/my-blog-content/2026-07-04--hugo-diagnostics/victor-hugo-067330a8-07d6-4f48-9d49-d8630f17f636.png"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2026-07-04--hugo-diagnostics/victor-hugo-067330a8-07d6-4f48-9d49-d8630f17f636.png"
---

<!-- Write your intro paragraph here. -->

# Hugo suddenly serving only 404s locally while GitHub Pages worked
*Trying something new here. I have in this post, asked Chat GPT to turn a full troubleshooting thread into a blog post. I did not edit it--maybe except a tiny one--, because my goal was to document this particular weird problem without really spending time on writing a blogpost. Actually I think the result is pretty good, sticking very nicely to reality. It is not in my voice or my style, but that's ok, I literally just wanted to document the thing and move on.*

## Symptoms

I noticed that newly created blog posts weren't appearing on my local Hugo server at `http://localhost:1313`.

Oddly, after deploying to GitHub Pages, the exact same posts appeared correctly online.

Initial hypothesis: perhaps Hugo wasn't noticing new content or was caching old pages.

---

## Discovery #1: I wasn't even talking to the correct Hugo server

Running `hugo serve` reported

```text
Web Server is available at http://localhost:51852/
```

but I had been habitually browsing to

```text
http://localhost:1313
```

It turned out an old Hugo process had been running for many hours.

```bash
lsof -i :1313 -n -P
```

revealed the stale process.

After killing it, a fresh `hugo serve` again bound to port 1313.

---

## Discovery #2: Everything returned 404

Unfortunately, even after killing the stale process, every request still returned a 404.

Not just the newest posts.

Every page.

Even pages that were known to exist on GitHub Pages.

Interestingly, `curl` produced the same result as Chrome and Firefox, ruling out browser cache issues.

---

## Discovery #3: Hugo does not emit HTTP access logs

One debugging instinct was to enable verbose logging.

```bash
hugo server --logLevel debug
```

Surprisingly, Hugo still produced no per-request logging.

This is expected behavior.

Hugo's debug logging is primarily for the build pipeline, not HTTP access logging.

---

## Discovery #4: Hugo still saw all of my content

Running

```bash
hugo list all
```

showed every expected page.

So this was **not** a content discovery problem.

The content existed.

The server simply wasn't rendering it.

---

## Discovery #5: Layout warnings suddenly became suspicious

I had been ignoring warnings like

```text
found no layout file for kind "page"
found no layout file for layout "post"
found no layout file for kind "section"
```

Originally I assumed they were harmless.

Once every page became a 404, they suddenly became the primary suspect.

If Hugo cannot locate any layouts, it has content but no templates with which to render it.

---

## Discovery #6: GitHub Actions was quietly doing something my laptop wasn't

The deployment workflow, `.github/workflows/gh-pages.yml`, contained

```yaml
submodules: true
```

which fetches the PaperMod theme during CI.

Locally I checked

```bash
git submodule status
```

and saw

```text
-266553fe... themes/PaperMod
```

The leading `-` indicates the submodule has **not been initialized**.

This was the clue.

---

## Root cause

My local checkout no longer had the PaperMod theme checked out.

GitHub Actions automatically initialized it during deployment.

My local machine did not.

Therefore:

* GitHub Pages had layouts.
* Local Hugo had no layouts.
* Hugo emitted layout warnings.
* Every request became a 404.

---

## Fix

```bash
git submodule update --init --recursive
```

Immediately afterwards

```bash
hugo serve
```

worked normally again.

---

## Lessons learned

* Don't ignore layout warnings from Hugo.
* `git submodule status` is worth learning to read.
* A leading `-` means the submodule has not been initialized.
* CI may be masking local problems by automatically fetching submodules.
* When local and CI disagree, compare the entire build environment, not just the Hugo version.
