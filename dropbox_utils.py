import dropbox
import os

print("Initializing Dropbox API...")

def make_client():
    return dropbox.Dropbox(os.getenv('DBX_ACCESS_TOKEN'))


def list_dir(loc):
    client = make_client()
    result = client.files_list_folder(path="")
    if result.entries:
        return [x.name for x in result.entries]
    

def read_file(loc):
    client = make_client()
    meta, response = client.files_download(loc)
    assert meta.path_lower == loc
    if response.status_code == 200:
        return response.text
