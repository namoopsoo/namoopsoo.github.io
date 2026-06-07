

default:
  just --list

append-images file *images:
  python quick_blog_post.py --append-only --existing-file {{file}} --images {{images}}

new-slug-info:
  # hugo new content/note/2026-mm-dd--slug.md
