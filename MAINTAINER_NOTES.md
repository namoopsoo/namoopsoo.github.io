# Maintainer Notes

These notes are for repository maintenance workflows.

## Quickly convert blog post images to S3 artifacts

This workflow expects `S3_DEPLOY_BUCKET` to be defined.

### Upload images to S3 and append HTML links to an existing Markdown file

```sh
python quick_blog_post.py \
    --append-only \
    --existing-file "/path/to/content/file.md" \
    --images "/full/path/to/image.png,/full/path/to/another_image.png"
```

### Convert local relative image links to S3 links and upload the images

```sh
python quick_blog_post.py \
    --convert-images-to-s3-assets \
    --existing-file "/path/to/content/file.md" \
    --local-asset-dir "/path/to/local/asset/dir"
```
