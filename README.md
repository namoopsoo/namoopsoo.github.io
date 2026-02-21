# namoopsoo.github.io

This repository contains the source for my public blog/site.

## Tech stack

- [Hugo](https://gohugo.io/) for static site generation
- Theme content and custom layouts in this repository

## Local development

```sh
hugo server -D
```

Then open `http://localhost:1313`.

## Build

```sh
hugo
```

The generated site output is written to `public/`.

## Maintainer notes

Operational scripts and personal workflow notes have been moved out of this README into `MAINTAINER_NOTES.md`.

## Giscus comments setup

This site includes optional support for [Giscus](https://giscus.app/) comments on post pages.

1. Go to https://giscus.app/ and connect it to your repository discussions.
2. Copy the generated values for repository + category IDs.
3. Update `_config.toml` under `[params.giscus]`:
   - set `enabled = true`
   - set `repo`, `repoid`, and `categoryid`
   - optionally adjust mapping/theme/language options

When enabled, the comment widget is rendered below post content.
