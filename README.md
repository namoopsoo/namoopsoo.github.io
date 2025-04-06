

### Quickly convert blog post images to S3 artifacts
This code expects `S3_DEPLOY_BUCKET` is defined.

## Examples

### upload images to s3 and append html links to them to an existing .md file
```sh
python quick_blog_post.py \
    --append \
    --existing-file "/path/to/content/file.md" \
    --images "/full/path/to/image.png,/full/path/to/another_image.png" \
```

### convert local relative image links to s3 links and upload the images
```sh
python quick_blog_post.py \
    --convert-images-to-s3-assets \
    --existing-file "/path/to/content/file.md" \
    --local-asset-dir "/path/to/local/asset/dir"
```