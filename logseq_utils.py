import requests
import os
import time

def get_block(block_uuid):
    token = os.getenv("LOGSEQ_TOKEN")
    url = "http://127.0.0.1:12315/api"
    headers = {"Content-Type": "application/json",
              "Authorization": f"Bearer {token}"}
    payload = {
    "method": "logseq.Editor.getBlock",  
      "args": [block_uuid, 
               {"includeChildren": True}]
    }
    # "args": ["Test page", "This is a new block", {"isPageBlock": true}]}
    response = requests.post(url, json=payload, headers=headers)
    return response


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
  


def get_page_blocks_tree(name):
    token = os.getenv("LOGSEQ_TOKEN")
    url = "http://127.0.0.1:12315/api"
    headers = {"Content-Type": "application/json",
              "Authorization": f"Bearer {token}"}
    payload = {
    "method": "logseq.Editor.getPageBlocksTree",  
      "args": [name]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response
  

def build_markdown_from_page_blocks(blocks):
    print("DEBUG", [x["level"] for x in blocks])
    time.sleep(1)

    stuff = []
    for block in blocks:
        stuff.append({"level": block["level"], "content": block["content"]})
        if block["children"]:
            stuff.extend(build_markdown_from_page_blocks(block["children"]))

    return stuff
