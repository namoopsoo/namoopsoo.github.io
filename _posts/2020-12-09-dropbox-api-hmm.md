---
date: 2020-12-09
title: Easy Blog Posting ("My Noting Book")
category: notes
---


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

##### step 1, get a reference.. like [here](https://developer.github.com/v3/git/refs/#get-a-reference)

```
curl -v -H "Authorization: token ${GITHUB_TOKEN}"   https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/ref/heads/master
```
Nice excellent, ...
```
...
...
{
  "ref": "refs/heads/master",
  "node_id": "MDM6UmVmMTAwMTg1NjcwOnJlZnMvaGVhZHMvbWFzdGVy",
  "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/refs/heads/master",
  "object": {
    "sha": "482d52f53a146dd688eff4ed8093cf2980580662",
    "type": "commit",
    "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/commits/482d52f53a146dd688eff4ed8093cf2980580662"
  }
}
```

##### step 2 , Grab the commit that HEAD points to

```
curl -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/commits/482d52f53a146dd688eff4ed8093cf2980580662
```

```
{
  "sha": "482d52f53a146dd688eff4ed8093cf2980580662",
  "node_id": "MDY6Q29tbWl0MTAwMTg1NjcwOjQ4MmQ1MmY1M2ExNDZkZDY4OGVmZjRlZDgwOTNjZjI5ODA1ODA2NjI=",
  "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/commits/482d52f53a146dd688eff4ed8093cf2980580662",
  "html_url": "https://github.com/namoopsoo/namoopsoo.github.io/commit/482d52f53a146dd688eff4ed8093cf2980580662",
  "author": {
    "name": "Michal Piekarczyk",
    "email": "namoopsoo",
    "date": "2020-12-13T21:39:11Z"
  },
  "committer": {
    "name": "Michal Piekarczyk",
    "email": "namoopsoo",
    "date": "2020-12-13T21:39:11Z"
  },
  "tree": {
    "sha": "e5a9ee9506a040a7cc8c608614db7531f8f32e70",
    "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/trees/e5a9ee9506a040a7cc8c608614db7531f8f32e70"
  },
  "message": "moar",
  "parents": [
    {
      "sha": "13db6ee453ea2b05d09ed8da1b7baa87fbbdcebc",
      "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/commits/13db6ee453ea2b05d09ed8da1b7baa87fbbdcebc",
      "html_url": "https://github.com/namoopsoo/namoopsoo.github.io/commit/13db6ee453ea2b05d09ed8da1b7baa87fbbdcebc"
    }
  ],
  "verification": {
    "verified": false,
    "reason": "unsigned",
    "signature": null,
    "payload": null
  }
}
```
* Ok and the tree sha is important. Reading up on this [here](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
* Okay after taking a [mini detour](/2020/12/13/Article-GitInternalsGitObjects-notes.html) to understand what a _Tree Object_ is, I think I can keep going now .
* So a _Tree Object_ is a group of other objects ( blob and or tree objects).
* So continuing with [this article](http://www.levibotelho.com/development/commit-a-file-with-the-github-api/) , going to post a blob next

#### 3. Post your new file to the server

```
curl \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/blobs \
  -d '{"content": "content of the blob", "encoding": "utf-8"}'
```

Getting

```
{
  "message": "Not Found",
  "documentation_url": "https://docs.github.com/rest/reference/git#create-a-blob"
}
```

Well Not Found is better than permission denied I guess.


* Ah actually, .. I took a random guess and looking at https://github.com/settings/tokens indeed found I needed to just add some extra permissions.
* Tried that same `curl -X POST` again and now got back

```
{
  "sha": "6b2d785ecc7db8b71ee933a5b22961a52f40592c",
  "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/blobs/6b2d785ecc7db8b71ee933a5b22961a52f40592c"
}
```

So all good.

#### 4. Get a hold of the tree that the commit points to
*  Ok so grabbing that `e5a9ee9506a040a7cc8c608614db7531f8f32e70` tree of my target branch's current `HEAD` commit now...
* ( and incidentally that `jq` json querying parsing utility is kind of nice here.. )
```
get /repos/{owner}/{repo}/git/trees/e5a9ee9506a040a7cc8c608614db7531f8f32e70
curl \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/trees/e5a9ee9506a040a7cc8c608614db7531f8f32e70  \
  | jq --color-output '.tree | .[0:3]'
  [
    {
      "path": ".gitignore",
      "mode": "100644",
      "type": "blob",
      "sha": "f40fbd8ba564ea28e0a2501e2921909467b39887",
      "size": 56,
      "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/blobs/f40fbd8ba564ea28e0a2501e2921909467b39887"
    },
    {
      "path": "404.html",
      "mode": "100644",
      "type": "blob",
      "sha": "086a5c9ea988c5a4d37acc5f8ea089e37cb19371",
      "size": 419,
      "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/blobs/086a5c9ea988c5a4d37acc5f8ea089e37cb19371"
    },
    {
      "path": "CNAME",
      "mode": "100644",
      "type": "blob",
      "sha": "922c44a4850e7421585c9030ecd82face732adc6",
      "size": 21,
      "url": "https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/blobs/922c44a4850e7421585c9030ecd82face732adc6"
    }
  ]


```

```
(pandars3) $ curl   -H "Accept: application/vnd.github.v3+json"   -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/repos/namoopsoo/namoopsoo.github.io/git/trees/e5a9ee9506a040a7cc8c608614db7531f8f32e70 |jq --color-output '.tree | map(.type)'
[
  "blob",
  "blob",
  "blob",
  "blob",
  "blob",
  "tree",
  "blob",
  "tree",
  "tree",
  "tree",
  "tree",
  "tree",
  "tree",
  "tree",
  "tree",
  "blob",
  "tree",
  "blob",
  "blob",
  "blob",
  "blob",
  "blob",
  "blob",
  "blob",
  "blob"
]
```

#### 5. Create a tree containing your new file
* Ok So I must create a new tree containing the newly created blob.
