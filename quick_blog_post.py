import argparse
import datetime
import frontmatter
import os
import re
import sys
from pathlib import Path

import s3utils as fs3


def bake_options():
    return [
            [['--verbose', '-v'],
                {'action': 'store_true',
                    'help': 'pass to to be verbose with commands'},
                ],
            [['--dry-run', '-D'],
                {'action': 'store_true',
                    'help': 'Dry run. Just print the command.  '},],
            [['--append'],
                {'action': 'store_true',
                    'help': 'Append instead of creating a new file. (If the file already exists, you will get an error.)'},],
            [['--images'],
                {'action': 'store',
                    'help': 'List of images to include, separated by a "," comma without spaces surrounding the comma'},],
            [['--out-dir'],
                {'action': 'store',
                    'help': 'Target directory. Optional if providing "--existing-file"'},],
            [['--existing-file'],
                {'action': 'store',
                    'help': 'Update an existing file. Otherwise, provide "--output-dir" '},],
            [['--title'],
                {'action': 'store',
                    'help': 'title'},],
            [['--date'],
                {'action': 'store',
                    'help': 'date'},],

            [['--stdout'],
                {'action': 'store_true',
                    'help': 'Send the html to stdout instead.'},],
            [['--only-convert-images-to-s3-assets'],
                {'action': 'store_true',
                    'help': 'For an existing file, send its local images to S3 and replace the links with S3 links.'},],
            [['--local-asset-dir'],
                {'action': 'store',
                    'help': 'Where to find local relative mentioned assets like images mentioned in the content (e.g. md ) file '},],
            [['--convert-img-to-hugo'],
             {"action": "store",
              "help": "<img> to hugo stuff."}]

                ]

    ##
    #             help='',
    #             default='',
    #             required='',
    #             choices='',
    #             action='',
    #             type='',


def parse_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d')


def header_template(date, title, category=None):
    print('parsed date', )
    return f'''---
layout: post
title: {title}
{'category: ' + category if category is not None else ''}
author: Michal
date: {date}  12:00 -0500
---

    '''

def write_post_file(path, content, append):
    if append:
        with open(path, 'a') as fd:
            fd.write(content)
    else:
        if os.path.exists(path):
            sys.exit(path, 'already exists. Please use --append')

        with open(path, 'w') as fd:
            fd.write(content)

    print('wrote to ', path)


def make_image_html(blah, hugo_format=True):
    """
    Note, here is what the hugo format looks like
    {{< figure src="{url}" width="50%">}}
    """
    if isinstance(blah, str):
        s3fn_vec = [blah]
    elif isinstance(blah, list):
        s3fn_vec = blah
    else:
        raise Exception("oops")

    if hugo_format:
        return "\n".join([
            (f'{{{{< figure src="{make_s3_image_url(x)}" width="50%">}}}}')
            for x in s3fn_vec])
    else:
        return '\n'.join([
            (f'<img src="{make_s3_image_url(x)}" width="50%">')
            for x in s3fn_vec])


def make_s3_image_url(loc):
    deploy_bucket = os.getenv("S3_DEPLOY_BUCKET")
    return f"https://s3.amazonaws.com/{deploy_bucket}/{loc}"


def upload_images_s3(images, prefix, dry_run=False):
    deploy_bucket = os.getenv('S3_DEPLOY_BUCKET')
    s3fn_vec = []
    for local_loc in images:
        with open(local_loc, 'rb') as fd:
            blah = fd.read()
        loc = os.path.basename(local_loc)
        s3fn = f'{prefix}/{loc}'
        s3fn_vec.append(s3fn)
        if dry_run:
            print(deploy_bucket, s3fn, len(blah))
        else:
            fs3.write_s3_file(deploy_bucket, s3fn, blah)
    return s3fn_vec


def make_prefix(date, title):
    year = parse_date(date).year
    return f"{year}/{date}-{title.replace(' ', '-')}"


def check_env_vars():
    deploy_bucket = os.getenv('S3_DEPLOY_BUCKET')
    
    return bool(deploy_bucket)

def convert_local_images_to_s3_assets(content_file_path, absolute_asset_dir, replace=True):
    """
    Args:
        content_file: the html or md file
        absolute_asset_dir: prepend to what is in the <img src=""> right now,
            to convert its relative path to find the image
    """
    output_lines = []
    lines = Path(content_file_path).read_text().split("\n")
    asset_dir = Path(absolute_asset_dir)
    images = []

    # first pass
    for line in lines:
        match_img_src = re.search(r"<img\s+src=\"([^\"]+)\"", line)
        match_img_md = re.search(r"!\[[^\[\]]+\]\(([^\(\)]+)\)", line)
        if match_img_src:
            relative_path = Path(match_img_src.groups()[0])
        elif match_img_md:
            relative_path = Path(match_img_md.groups()[0])
        else:
            relative_path = ""
        if relative_path and not str(relative_path).startswith("http"):
            assert " " not in str(relative_path), relative_path
            image_path = asset_dir / relative_path
            assert image_path.exists(), image_path
            images.append(image_path)

    print("Ok cool now we know all the images exist. Going to upload,", 
            [x.name for x in images])
    if not images:
        print("Nothing to do.")
        return

    post = frontmatter.loads(Path(content_file_path).read_text())
    date, title = str(post.to_dict()["date"]), post.to_dict()["title"]
    assert date
    assert title

    prefix = make_prefix(date=date, title=title)
    s3fn_vec = upload_images_s3(images, prefix, dry_run=False)
    print(s3fn_vec)

    # mapping = {k: make_s3_image_url(k) for k in s}

    print("Pass two now")

    # second pass
    for line in lines:
        match_img_src = re.search(r"(?P<all><img\s+src=\"(?P<path>[^\"]+)\"[^>]+>)", line)
        match_img_md = re.search(r"(?P<all>!\[[^\[\]]+\]\((?P<path>[^\(\)]+)\))", line)
        if match_img_src:
            relative_path = Path(match_img_src.groupdict()["path"])
            all_match = Path(match_img_src.groupdict()["all"])
        elif match_img_md:
            relative_path = Path(match_img_md.groupdict()["path"])
            all_match = Path(match_img_md.groupdict()["all"])
        else:
            relative_path = ""
        if relative_path:
            image_path = asset_dir / relative_path
            assert image_path.exists(), image_path
            import ipdb;ipdb.set_trace()

            updated_line = line.replace(
                str(all_match), 
                make_image_html(
                    # make_s3_image_url(str(Path(prefix) / relative_path.name))
                    (str(Path(prefix) / relative_path.name))
                ),
            )
            if line == updated_line:
                print("Hmm, line and updated_line are both ", line, ", that is weird")
            output_lines.append(updated_line)
        else:
            output_lines.append(line)
    if replace:
        out = Path(content_file_path).write_text("\n".join(output_lines))
        print("write out", out)
        

def update_this_file(loc, update_in_place=True):
    """
    Update <img src=..> to {{<figure src="">}} hugo style 
    """
    lines = Path(loc).read_text().splitlines()
    vec = []
    for line in lines:
            if m := re.search(r'(?P<line><img\s+src="(?P<url>[^"]+)"\s+(width="(?P<width>\d+%)")?\s*(/)?>)', line):
                    url = m.groupdict()["url"]
                    if width := m.groupdict()["width"]:
                            width_part = f'width="{width}"'
                    else:
                            width_part = ""
                    updated = f'{{{{< figure src="{url}" {width_part} >}}}}'
                    updated_line = line.replace(m.groupdict()["line"], updated)
                    print("replacing: ", line, updated_line)
                    vec.append(updated_line)
            else:
                    vec.append(line)
    if update_in_place:
            Path(loc).write_text("\n".join(vec))    
    else:
            print("done")


def do():
    parser = argparse.ArgumentParser()

    [parser.add_argument(*x[0], **x[1])
            for x in bake_options()]

    # Collect args from user.
    args = vars(parser.parse_args())

    if not check_env_vars():
        print("Oops need to set S3_DEPLOY_BUCKET")
        return

    existing_file = args.get("existing_file")
    if args.get("only_convert_images_to_s3_assets"):

        assert existing_file and Path(existing_file).is_file()
        local_asset_dir = args.get("local_asset_dir")
        assert local_asset_dir and Path(local_asset_dir).is_dir()
        convert_local_images_to_s3_assets(existing_file, local_asset_dir)
        print("Done.")
        return

    images = [x.replace("\\", "").strip() for x in args.get("images").split(",")]
    print("images", images)
    dry_run = args.get("dry_run")
    title = args.get("title")
    date = args.get("date")
    out_dir = args.get("out_dir")
    assert existing_file or out_dir

    print(args)
    if existing_file:
        prefix = os.path.basename(existing_file)
        if prefix.endswith('.md'):
            prefix = prefix[:-3]
    else:
        prefix = make_prefix(date=date, title=title)
    print('prefix', prefix)
    s3fn_vec = upload_images_s3(images, prefix, dry_run=dry_run)

    image_html = make_image_html(s3fn_vec)

    header_html = header_template(date, title)

    print('image_html', image_html)
    append = args.get('append')
    if append:
        content = f'\n{image_html}'
    else:
        content = f'{header_html} \n{image_html}'

    if args.get('stdout'):
        print(content)
    else:
        if existing_file:
            path = existing_file
        else:
            path = f"{out_dir}/{date}-{title.replace(' ', '-')}.md"
        write_post_file(path=path,
                        content=content,
                        append=append)
    

if __name__ == "__main__":    
    do()
