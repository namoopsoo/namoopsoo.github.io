


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


### 2020-12-13

#### oh my special app folder was created w/ the acess token
* As soon as on my [app page](https://www.dropbox.com/developers/apps/info/blahblahblah) I hit "Generate access token" , my special App folder was created.


```python
import dropbox
import os

print("Initializing Dropbox API...")
dbx = dropbox.Dropbox(os.getenv('DBX_ACCESS_TOKEN'))
result = dbx.files_list_folder(path="")

```
```python
BadInputError: BadInputError('xxxxxxxxxxx', 'Error in call to API function "files/list_folder": Your app is not permitted to access this endpoint because it does not have the required scope \'files.metadata.read\'. The owner of the app can enable the scope for the app using the Permissions tab on the App Console.')
```
* Ah ok so I went to the Permissions tab, checked that  'files.metadata.read' box and tried again.
* Now seeing

```python
AuthError: AuthError('xxxxxxxxxxx', AuthError('missing_scope', TokenScopeError(required_scope='files.metadata.read')))
```
* Ah according to [stackoverflow](https://stackoverflow.com/a/64201654) , the scope cannot be retroactively granted to a token created before the scope was granted.
* Ok ... trying to re-create a new token...
* Ok recreated. Retried. Worked!
* How to read?
* What's the difference between the two `files/download` , `files/export`  ( `files/get_preview` )
```python
print("Initializing Dropbox API...")
dbx = dropbox.Dropbox(os.getenv('DBX_ACCESS_TOKEN'))
meta, response = dbx.files_download('/blarg.txt')

# In [22]: response.text                                                                                                                        
# Out[22]: 'foo blarg\n'
```

#### Github interaction
* Hmm I was going down the path of building an AWS Batch container to commit to my git repo
* But hmmm I encountered that there may be a [Github API](https://docs.github.com/en/free-pro-team@latest/rest) which I can perhaps use??? And a [nice tutorial](https://codesnippet.io/github-api-tutorial/)
* Cool, so `https://api.github.com/users/namoopsoo/repos` , repos are here.
* However [the oauth flow](https://docs.github.com/en/free-pro-team@latest/rest/overview/other-authentication-methods)  , looks kind of involved for a quick script
* But ah that's right you can create a token for your account from here,  [Github settings](https://github.com/settings/tokens/new) .
* Ok cool I was able to perform a simple curl w/ the personal token I created for myself ...  ( per [docs](https://docs.github.com/en/free-pro-team@latest/rest/overview/other-authentication-methods) )

```
$ curl -v -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/users/namoopsoo/repos
```

#### ok but can your write using this API is the big question..
* Hmm according to [here](https://docs.github.com/en/free-pro-team@latest/rest/reference/git#commits) you can commit.

```
post /repos/{owner}/{repo}/git/commits
```
* But not seeing how to include the actual diffs in there. Maybe a [blob?](https://docs.github.com/en/free-pro-team@latest/rest/reference/git#blobs)
* Ok according to [this nice article](http://www.levibotelho.com/development/commit-a-file-with-the-github-api/)  , indeed the blob endpoint is for files! hmm

```

```
