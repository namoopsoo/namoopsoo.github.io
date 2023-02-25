

### Quickly convert blog post images to S3 artifacts
This code expects `S3_DEPLOY_BUCKET` is defined.

```sh
python quick_blog_post.py \
    --only-convert-images-to-s3-assets \
    --existing-file "/path/to/content/file.md" \
    --local-asset-dir "/path/to/local/asset/dir"
```
