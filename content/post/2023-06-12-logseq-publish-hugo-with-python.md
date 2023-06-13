---
date: 2023-06-12
title: logseq publish hugo with python
---
public:: true
blog-date:: 2023-06-12
# briefly
Inspired by the super popular #[[schrodinger logseq plugin]], I wrote up something in #python today, to publish to #Hugo like https://github.com/sawhney17/logseq-schrodinger but also with support for block embeds.

In particular, I was also really inspired by [[Bas Grolleman]]'s concept [here](https://youtu.be/CPMuGn2d8po)  around how to be able to use #interstitial-journaling and be able to nicely coalesce selected sources through their block embeds, into a target logseq concept they all refer to.
## Full code from this blog post
By the way, this code is still just at the "first stab" / #proof-of-concept stage, but it is here, 
https://github.com/namoopsoo/logseq_utils
### And usage is just below
Say you have a page "blogpost/2023-06-12-name-of-your-logseq-page" , where you happen to use embeds like, 
```
{{embed ((64864e08-de92-4127-9162-8b5b946b021b))}}
```
then to create a markdown file like "content/post/2023-06-12-name-of-your-logseq-page.md" , locating it in "content/post/" say if that is your Hugo post location, then use,
```python
from pathlib import Path
import logseq_utils as lu

page = "blogpost/2023-06-12-name-of-your-logseq-page"
filename = page.split("/")[1] + ".md"
target_dir = "content/post/"
target_loc = str(Path(target_dir) / filename)
print("target_loc", target_loc)
# target_loc content/post/2023-06-12-logseq-publish-hugo-with-python.md

lu.build_markdown(page, target_loc)
```

# The logseq REST API
## Would have loved to help w/ logseq-schrodinger but
Ideally I would love to attempt a pull request on https://github.com/sawhney17/logseq-schrodinger  , and I have left the block embed as a feature idea  [here](https://github.com/sawhney17/logseq-schrodinger/issues/35), but my knowledge of the logseq [dev setup](https://github.com/logseq/logseq/blob/master/docs/develop-logseq.md) , including Clojure Script and react is smaller than my desire to first get something working to help solve my immediate problem hah 😅.
## But the logseq REST API looks great!
According to https://docs.logseq.com/#/page/local%20http%20server , and https://plugins-doc.logseq.com , looks like one just needs to add a local API token and then you are basically ready to interact with your logseq using "127.0.0.1:12315"
# Iterating
## Using getPageBlocksTree gave the blocks on a page
### Like this
id:: 6487a8b5-ac96-4a45-aa2a-28bbc7002aa4
```python
def get_page_blocks_tree(name, include_children=False):
    token = os.getenv("LOGSEQ_TOKEN")
    url = "http://127.0.0.1:12315/api"
    headers = {"Content-Type": "application/json",
              "Authorization": f"Bearer {token}"}
    payload = {
    "method": "logseq.Editor.getPageBlocksTree",  
      "args": [name, 
               {"includeChildren": include_children}]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response
  
```

### A stab at a recursive call here
13:51 ok some simple stab at using this API then, to build #[[log-seq markdown hugo integration]] [[Hugo]]
id:: 64875626-e55d-4613-9351-e6a5806e8912
14:27 ok, wrote some code in `log_utils.py` , and running,
```python
import requests
import time

def build_markdown_from_page_blocks(blocks):
    print("DEBUG", [x["level"] for x in blocks])
    time.sleep(1)

    stuff = []
    for block in blocks:
        stuff.append({"level": block["level"], "content": block["content"]})
        if block["children"]:
            stuff.extend(build_markdown_from_page_blocks(block["children"]))

    return stuff

```
```python
page = "blogpost/2023-06-11-semantic-code-search-first-stab"
response = lu.get_page_blocks_tree(page)
response.status_code
blocks = response.json()
len(blocks)  # 4

stuff = lu.build_markdown_from_page_blocks(blocks)
```
ok nice haha worked on first try as intended #moment/satisfaction 😀

```sh
In [57]: stuff = lu.build_markdown_from_page_blocks(blocks)
DEBUG [1, 1, 1, 1]
DEBUG [2, 2]
DEBUG [3, 3, 3]
DEBUG [2, 2, 2, 2, 2, 2, 2]
DEBUG [3, 3]


[{'level': 1, 'content': 'public:: true'},
 {'level': 1, 'content': ''},
 {'level': 1, 'content': '# Initial Learnings'},
 {'level': 2,
  'content': '## Learned about [[symmetric vs asymmetric semantic search]]'},
 {'level': 3,
  'content': 'This distinction refers to #[[sentence similarity task]] where the query is of the same size or asymmetrically, smaller size, such as a one or two word query.'},
 {'level': 3, 'content': 'And wow that is exactly what. Iwas looking for !'},
 {'level': 3, 'content': 'So apparently this includes the "msmarco" models.'},
 {'level': 2, 'content': ''},
 {'level': 1, 'content': '# Final test run'},
 {'level': 2,
  'content': 'Idea is to build a corpus with, hey why not, the code from the #sentence-transformers repo.'},
 {'level': 2,
  'content': 'Had a few test runs today, iterating on the approach, using queries from files other than the ones I built a corpus for , #moment/doh haha . Also weirdly the msmarco model documented as the v3 that should be used is MIA somehow, but the v2 seems fine. And "msmarco-MiniLM-L-6-v3" is fine too. \n\nBut here is the last run for today.'},
 {'level': 2, 'content': '{{embed ((64864e08-de92-4127-9162-8b5b946b021b))}}'},
 {'level': 2, 'content': '## And code for building that corpus'},
 {'level': 3, 'content': '{{embed ((648728d8-5958-4df6-95d4-b81de6665974))}}'},
 {'level': 3, 'content': ''},
 {'level': 2, 'content': ''},
 {'level': 2, 'content': ''},
 {'level': 2, 'content': ''}]
```

### And then filling out the embeds
14:47 ok just need to fill the embeds with the block embed outputs then,
id:: 648764a3-6ede-4550-82cf-5ce07e765ac0
14:56, 
```python
import re
block = {"content": "{{embed ((648728d8-5958-4df6-95d4-b81de6665974))}}"}
if match := re.match(
  r"^{{embed \(\(([a-zA-Z0-9-]+)\)\)}}$",
  block["content"]
):
    print("yes", match.groups()[0])

# yes 648728d8-5958-4df6-95d4-b81de6665974
```
hmm so for instance if we have the block below, which is at level 3, 
```python
{'properties': {},
      'unordered': True,
      'parent': {'id': 28919},
      'children': [],
      'id': 29214,
      'pathRefs': [{'id': 28906}, {'id': 29113}, {'id': 29220}],
      'level': 3,
      'uuid': '64875997-b4fd-4079-9a06-19b1606d5f33',
      'content': '{{embed ((648728d8-5958-4df6-95d4-b81de6665974))}}',
      'journal?': False,
      'macros': [{'id': 29221}],
      'page': {'id': 28906},
      'left': {'id': 28919},
      'format': 'markdown',
      'refs': [{'id': 29113}, {'id': 29220}]}
```
And we fetch the block "648728d8-5958-4df6-95d4-b81de6665974" ,
collapsed:: true
```python
In [59]: block_uuid = "648728d8-5958-4df6-95d4-b81de6665974"

In [60]: response = lu.get_block(block_uuid)

In [61]: response.json()
Out[61]: 
{'properties': {'id': '648728d8-5958-4df6-95d4-b81de6665974'},
 'parent': {'id': 28846},
 'children': [{'properties': {},
   'parent': {'id': 29113},
   'children': [],
   'id': 29219,
   'pathRefs': [{'id': 28},
    {'id': 1967},
    {'id': 5812},
    {'id': 27790},
    {'id': 27795},
    {'id': 28383},
    {'id': 28504},
    {'id': 28556},
    {'id': 28906},
    {'id': 28907}],
   'level': 1,
   'uuid': '64875a31-5142-4f50-a542-5d5c00021cb4',
   'content': 'Put the following into a file `code_search.py`\n```python\nfrom pathlib import Path\nfrom itertools import chain\n\n\ndef build_texts_from_repository(repo_dir):\n    """Return a dataset of the code\n    """\n    dataset = []\n    file_types = []\n    for path in chain(\n        Path(repo_dir).glob("**/*.py"),\n        Path(repo_dir).glob("**/*.md"),\n    ):\n        assert path.is_file() and path.suffix\n        lines = path.read_text().splitlines()\n        \n        dataset.extend(\n            [{"line_number": i,\n               "line": line,\n               "path": str(path.relative_to(repo_dir))}\n        for i, line in enumerate(lines)\n         ]\n        )\n    return dataset\n\n```',
   'page': {'journalDay': 20230611,
    'name': 'jun 11th, 2023',
    'originalName': 'Jun 11th, 2023',
    'id': 28504},
   'left': {'id': 29113},
   'format': 'markdown'},
  {'properties': {},
   'parent': {'id': 29113},
   'children': [],
   'id': 29218,
   'pathRefs': [{'id': 28},
    {'id': 1967},
    {'id': 5812},
    {'id': 27790},
    {'id': 27795},
    {'id': 28383},
    {'id': 28504},
    {'id': 28556},
    {'id': 28906},
    {'id': 28907}],
   'level': 1,
   'uuid': '64875a2e-7b2a-47fb-891b-419cd3347643',
   'content': '```python\nimport os\nimport code_search as cs\nfrom pathlib import Path\nrepos_dir = os.getenv("REPOS_DIR")\ntarget_dir = Path(repos_dir) / "sentence-transformers"\ndataset = cs.build_texts_from_repository(target_dir)\n\n```\ndouble checking , \n```python\n\nIn [12]: dataset[:10]\nOut[12]: \n[{\'line_number\': 0,\n  \'line\': \'from setuptools import setup, find_packages\',\n  \'path\': \'setup.py\'},\n {\'line_number\': 1, \'line\': \'\', \'path\': \'setup.py\'},\n {\'line_number\': 2,\n  \'line\': \'with open("README.md", mode="r", encoding="utf-8") as readme_file:\',\n  \'path\': \'setup.py\'},\n {\'line_number\': 3,\n  \'line\': \'    readme = readme_file.read()\',\n  \'path\': \'setup.py\'},\n {\'line_number\': 4, \'line\': \'\', \'path\': \'setup.py\'},\n {\'line_number\': 5, \'line\': \'\', \'path\': \'setup.py\'},\n {\'line_number\': 6, \'line\': \'\', \'path\': \'setup.py\'},\n {\'line_number\': 7, \'line\': \'setup(\', \'path\': \'setup.py\'},\n {\'line_number\': 8,\n  \'line\': \'    name="sentence-transformers",\',\n  \'path\': \'setup.py\'},\n {\'line_number\': 9, \'line\': \'    version="2.2.2",\', \'path\': \'setup.py\'}]\n\nIn [13]: set([Path(x["path"]).suffix for x in dataset])\nOut[13]: {\'.md\', \'.py\'}\n```',
   'page': {'journalDay': 20230611,
    'name': 'jun 11th, 2023',
    'originalName': 'Jun 11th, 2023',
    'id': 28504},
   'left': {'id': 29219},
   'format': 'markdown'}],
 'id': 29113,
 'pathRefs': [{'id': 28},
  {'id': 1967},
  {'id': 5812},
  {'id': 27790},
  {'id': 27795},
  {'id': 28383},
  {'id': 28504},
  {'id': 28556},
  {'id': 28906},
  {'id': 28907}],
 'propertiesTextValues': {'id': '648728d8-5958-4df6-95d4-b81de6665974'},
 'uuid': '648728d8-5958-4df6-95d4-b81de6665974',
 'content': 'ok cool, let me just focus on markdown and python\nid:: 648728d8-5958-4df6-95d4-b81de6665974',
 'page': {'journalDay': 20230611,
  'name': 'jun 11th, 2023',
  'originalName': 'Jun 11th, 2023',
  'id': 28504},
 'left': {'id': 29215},
 'format': 'markdown',
 'refs': [{'id': 29214}]}


```

15:12 hmm strangely it does not have its own level and its children start from level 1, so maybe this is meant to be incremental sort of.
15:26 ok added some kind of offset then
```python
def build_markdown_from_page_blocks(blocks, level_offset=0):
    print("DEBUG", [x["level"] for x in blocks])

    stuff = []
    for block in blocks:

        # Replace embed
        if match := re.match(
            r"^{{embed \(\(([a-zA-Z0-9-]+)\)\)}}$",
            block["content"]
        ):
            block_uuid = match.groups()[0]
            print("yes", block_uuid)

            response = get_block(block_uuid)
            assert response.status_code == 200

            new_block = response.json()
            new_block["level"] = block["level"]

            stuff.append({"level": new_block["level"], "content": new_block["content"]})
            if new_block["children"]:
                stuff.extend(
                    build_markdown_from_page_blocks(
                        new_block["children"],
                        level_offset=(level_offset + new_block["level"])
                    ))

        else:
            stuff.append(
                {"level": block["level"] + level_offset,
                 "content": block["content"]})
            if block["children"]:
                stuff.extend(
                    build_markdown_from_page_blocks(
                        block["children"], level_offset=level_offset)
                )

    return stuff

```


### And the markdown output
15:26 ok then now , to generate the markdown,
id:: 64877179-6d5e-4a1a-88ef-7826edf78ee5
Did this in a super simple way,
```python
def build_markdown(page_name, target_loc):
    response = get_page(page_name)
    assert response.status_code == 200 and response.json()

    response = get_page_blocks_tree(page_name)
    assert response.status_code == 200 and response.json()
    blocks = response.json()

    blog_date = blocks[0]["properties"]["blogDate"]

    stuff = build_markdown_from_page_blocks(blocks)

    page_title = page_name.split("/")[1]  # 
    if match := re.match(r"(\d{4}-\d{2}-\d{2})-(.*)", page_title):
        date_from_title, page_title = match.groups()
    print("page_title", page_title)

    page_title = page_title.replace("-", " ")
    print("page_title", page_title)

    text = [
        "---",
        f"date: {date_from_title}",
        f"title: {page_title}",
        "---",
    ] + [x["content"] for x in stuff]
    path = Path(target_loc)
    assert path.parent.is_dir()

    path.write_text("\n".join(text))
    ...

```
15:50 ok lets try this, 
```python
target_dir = "content/post/"
# 2023-06-12-spinoza-vs-descartes.md
page = "blogpost/2023-06-11-semantic-code-search-first-stab"
filename = page.split("/")[1] + ".md"
target_loc = str(Path(target_dir) / filename)
print("target_loc", target_loc)
# 'content/post/2023-06-11-semantic-code-search-first-stab.md'
lu.build_markdown(page, target_loc)
```
So per above, the first page built ended up being [this page](/post/2023-06-11-semantic-code-search-first-stab/)
And the second page was actually [this one](/post/2023-06-12-logseq-publish-hugo-with-python/)

## Some tips
### no hyphens in your API token
Oddly enough I was getting 
```
Out[12]: {'statusCode': 401, 'error': 'Unauthorized', 'message': 'Access Denied!'}
```
and then switched to a token without hyphens and it was fine.
### The right REST endpoint
Initially I was getting a `404` `'Route POST:/ not found'` when hitting
```
url = "http://127.0.0.1:12315"
```
as opposed to 
```
url = "http://127.0.0.1:12315/api"
```
### getPage returned no children
Oddly enough, hitting https://plugins-doc.logseq.com/logseq/Editor/getPage on a valid page, even with setting `includeChildren` to `true`, I was getting a `200` but an empty response payload.
However, I found using https://plugins-doc.logseq.com/logseq/Editor/getPageBlocksTree gave me all the child blocks for a page. 

Maybe that is the intended behavior, but I'm not sure.
### Retrieving a page with a literal slash worked but not with the "%2F"
12:52 let me try getting a page too,
id:: 64874d2d-6999-48bb-b19a-a6cba44c4f96
```python
def get_page(name, include_children=False):
    token = os.getenv("LOGSEQ_TOKEN")
    url = "http://127.0.0.1:12315/api"
    headers = {"Content-Type": "application/json",
              "Authorization": f"Bearer {token}"}
    payload = {
    "method": "logseq.Editor.getPage",  
      "args": [name, 
               {"includeChildren": include_children}]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response
  
response = get_page(
    "blogpost%2F2023-06-11-semantic-code-search-first-stab"
)
response.status_code
```
hmm weird saying it got a page but response.json() is null.
Ok, trying by id now, and below, this is working now,
```python
response = get_page(28504)

In [12]: response.json()
Out[12]: 
{'updatedAt': 1686580509936,
 'journalDay': 20230611,
 'createdAt': 1686463272305,
 'id': 28504,
 'name': 'jun 11th, 2023',
 'uuid': '648728d8-8c86-4afd-8bb2-4cd519ec4c76',
 'journal?': True,
 'originalName': 'Jun 11th, 2023',
 'file': {'id': 28527},
 'format': 'markdown'}

```
ok but then how to get a page by name then?
13:06 ok interesting, so I tried again but this time instead of the "%2F" where the "/" forward slash is, using the literal, and now worked !
collapsed:: true
```python

In [13]: response = get_page(
    ...:     "blogpost/2023-06-11-semantic-code-search-first-stab"
    ...: )
    ...: response.status_code
Out[13]: 200

In [14]: response.json()
Out[14]: 
{'properties': {'public': True},
 'updatedAt': 1686526563885,
 'createdAt': 1686526225155,
 'id': 28906,
 'propertiesTextValues': {'public': 'true'},
 'name': 'blogpost/2023-06-11-semantic-code-search-first-stab',
 'uuid': '648728d8-d545-42ce-b487-986d6cac3d55',
 'journal?': False,
 'originalName': 'blogpost/2023-06-11-semantic-code-search-first-stab',
 'file': {'id': 28909},
 'namespace': {'id': 28907},
 'format': 'markdown'}


```
ok

