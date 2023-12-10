---
title: Exporting messages from Apple imessages
date: 2023-12-09
---

# The problem
    Messages have been clogging up my iphone for a while now and at this point, they are taking up maybe 15Gigs. Most of this is photo attchments. I thought an options was to manually go through the phone UI, deleting photo attachments to save space, but I did a bit of this tedium and the storage space did not seem to clear up. Maybe it is delayed? The other alternative is to hit a button that says "only keep messages up to a year old". In reality, I don't need the 15 Gigs of photo attachments, but I don't want to lose the text data. 

# Mac laptop based export
Luckily a month or two ago I started syncing imessages through icloud and so I was able to try out [ReagentX's imessage-exporter](https://github.com/ReagentX/imessage-exporter) on github. Looks like this only pulled scattered `1meg` ofconversations, for sure only from this last month or two. 

I am on macos Ventura so I could not do the itunes backup as stated in the [reddit thread](https://www.reddit.com/r/apple/comments/10cp8dh/i_wanted_to_be_able_to_exportbackup_imessage/) , but I tried the unencrypted iphone backup that you can use just when you connect your phone to your laptop. In this backup there was a `Manifest.db` , which allowed me to find a `sms.db` in there and also Attachments. I was able to also use `imessage-exporter` on this `sms.db`, however the `--attachment-root` option looks like was not supported for iphone based extraction with the version I tried. Still, now I have an additional `13meg` of text data. 

# Note on using the `Manifest.db` in the iphone export
The `imessage-exporter` was not handling the 15gig of attachments I pulled from the iphone export at least now, but just writing out here what I did just in case this is available in the future. 

First I used ChatGPT to quickly cook up some `sqlite` code to inspect this `Manifest.db`, and then to pull out the table to csv, 

```python
import sqlite3
from pathlib import Path


def get_table_schemas(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    table_schemas = {}

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        schema = {}
        for column in columns:
            column_name = column[1]
            data_type = column[2]
            not_null = column[3]
            default_value = column[4]
            primary_key = column[5]
            schema[column_name] = {
                "data_type": data_type,
                "not_null": not_null,
                "default_value": default_value,
                "primary_key": primary_key
            }
        
        table_schemas[table_name] = schema

    conn.close()
    return table_schemas

def print_schemas(schemas):
    for table_name, schema in schemas.items():
        print(f"Table: {table_name}")
        for column_name, column_info in schema.items():
            print(f"  Column: {column_name}")
            print(f"    Data Type: {column_info['data_type']}")
            print(f"    Not Null: {column_info['not_null']}")
            print(f"    Default Value: {column_info['default_value']}")
            print(f"    Primary Key: {column_info['primary_key']}")

def export_table_to_csv(database_file, table_name, csv_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(data)

    conn.close()

```

So looking at the schema, with `print_schemas` , I saw two tables, `Files` and `Properties`. And I extracted both, like, 

```python
path = (Path("/Users/michal/Library/Application Support/MobileSync")
       / "Backup/00008020-000E7C903A23002E" / "Manifest.db")

import pandas as pd
import csv
export_table_to_csv(str(path), "Files", 
                    str(path.with_stem(path.stem + "-Files").with_suffix(".csv")))
export_table_to_csv(str(path), "Properties", 
                    str(path.with_stem(path.stem + "-Properties").with_suffix(".csv")))

manifestdf = pd.read_csv(path.with_suffix(".csv"))

```
I did a search for `sms` like, 

```python
manifestdf[(manifestdf.relativePath.notnull()) 
           & (manifestdf.relativePath.str.contains("sms"))][[
           "fileID","domain","relativePath"]].to_dict(orient="records")
```
which dug out,  this `sms.db` , 
```python
 {'fileID': '3d0d7e5fb2ce288813306e4d4636395e047a3d28',
  'domain': 'HomeDomain',
  'relativePath': 'Library/SMS/sms.db'},
```
I did also notice  "Library/SMS/Attachments/" , "Library/SMS/Drafts/"  in there, so I tried digging out the Attachments like this ,

```python

attachments_records = manifestdf[
    (manifestdf.relativePath.notnull()) 
    & (manifestdf.relativePath.str.contains("SMS/Attachments"))
    ][["fileID","domain","relativePath"]].to_dict(orient="records")
```
Somehow a lot of the data appeared to be missing, somehow, so I filtered by not missing, 
```python
source_dir = (Path("/Users/michal/Library/Application Support/MobileSync")
        / "Backup/00008020-000E7C903A23002E")
destination_dir = (
    Path("/Users/michal/imessage-data")
    / "2023-12-09-1934-from-iphone-hmm"
    / "Attachments"
	)
attachments_exist = []
for x in attachments_records:
    if (source_dir / x["fileID"][:2] / x["fileID"]).exists():
        attachments_exist.append(x)

attachments_exist[:2]
# [{'fileID': '7112c681ea44f8b64609aa943b5b1182a393136a',
#   'domain': 'MediaDomain',
#   'relativePath': 'Library/SMS/Attachments/61/01/72A08FCD-CD0B-4AF7-83CF-F5E94D546A64/IMG_1976.PNG'},
#  {'fileID': '1faae24aef070aebc630d8b315b1630f2ffc5be3',
#   'domain': 'MediaDomain',
#   'relativePath': 'Library/SMS/Attachments/61/01/FA8E24CD-AF3D-4607-B954-347E5DEF57AA/IMG_0714.jpeg'}]
```
After some trial and error, I ended up with this for the copy, 
```python
def copy_attachments(attachments_records, source_dir, destination_dir):
    for record in attachments_records:
        first_two_characters = record["fileID"][:2]
        from_path = source_dir / first_two_characters / record["fileID"]
        if from_path.exists():
            relative_path = Path("/".join(record["relativePath"].split("/")[3:]))
            to_path = destination_dir / relative_path
            if not to_path.parent.exists():
                to_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(from_path, to_path)
            ...
        ...
```
Though as I mentioned earlier, the imessage export call,  basically did not work. The diagnostics option ignores the attachments, 
```sh
imessage-exporter     --db-path /Users/michal/imessage-data/2023-12-09-1934-from-iphone-hmm/sms.db   --attachment-root /Users/michal/imessage-data/2023-12-09-1934-from-iphone-hmm/Attachments  --diagnostics   
Building cache...
[1/4] Caching chats...
[2/4] Caching chatrooms...
[3/4] Caching participants...
[4/4] Caching reactions...
Cache built!

iMessage Database Diagnostics

Contacts with more than one ID: 49
Message diagnostic data:
    Total messages: 76650
    Messages not associated with a chat: 2112
    Messages belonging to more than one chat: 26
Attachment diagnostic data:
    Total attachments: 16272
        Data referenced in table: 16.15 GB
        Data present on disk: 0.00 B
    Missing files: 16272 (100%)
        No path provided: 189
        No file located: 16083
Global diagnostic data:
    Total database size: 171.45 MB
    Duplicated contacts: 74
    Duplicated chats: 6
Done!
```
And later also, using the `--platform iOS` option I saw that the `--attachment-root` option is only supported for `--platform macOS` , so I am stuck at this point. But maybe later this can be worked out. 

In any case, the good news is that I was able to dig out the text data, which was more important to me and now I feel more comfortable to just go with the "only keep 1 years worth of data " option, moving forward 😀.
