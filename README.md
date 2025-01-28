

### Quickly convert blog post images to S3 artifacts
This code expects `S3_DEPLOY_BUCKET` is defined.


upload assets to s3,

```sh
python quick_blog_post.py \
    --existing-file "/path/to/content/file.md" \
    --local-asset-dir "/path/to/local/asset/dir"
    --images "/full/path/to/image.png,/full/path/to/another_image.png" \
    --append
```


dont remember what this is fully though
```sh
python quick_blog_post.py \
    --only-convert-images-to-s3-assets \
    --existing-file "/path/to/content/file.md" \
    --local-asset-dir "/path/to/local/asset/dir"
```
