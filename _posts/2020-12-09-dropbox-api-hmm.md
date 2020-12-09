


### For my EasyBlogPosting project..
Testing out the Dropbox API..

### 2020-12-09

#### trying this out
* Per [here](https://www.dropbox.com/developers/reference/getting-started) ...
```python
pip install dropbox
```

#### Went w/ that Getting Started page
* Through that page, I created a new test app for myself.

* Using the API explorer ... I hit Get Token ..

https://www.dropbox.com/oauth2/authorize?response_type=token&client_id=xxxxxxxxx&redirect_uri=https%3A%2F%2Fdropbox.github.io%2Fdropbox-api-v2-explorer%2F&state=file_requests_list!39%2B%2Bxxxxxxxx&token_access_type=online&

* That generated a token and I used https://dropbox.github.io/dropbox-api-v2-explorer/#files_list_folder and I was able to see actual folders in my account.
* That's cool except I thought I had chosen  something like 'single folder access' so I'm slightly confused why I can see the other folders.
* Maybe the generated token in the API explorer is separate and meant for testing. Hopefully it's short lived.
