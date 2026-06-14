

default:
  just --list

append-images file *images:
  python quick_blog_post.py --append-only --existing-file {{file}} --images {{images}}

new-slug-info:
  # just wrote this here as a reminder of how easy it already is to use hugo new to create a new slug
  # hugo new content/note/2026-mm-dd--slug.md
