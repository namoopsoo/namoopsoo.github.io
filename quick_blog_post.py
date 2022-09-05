import argparse
import datetime
import os
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
                    'help': 'List of images to include'},],
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


def make_image_html(s3fn_vec):
    deploy_bucket = os.getenv('S3_DEPLOY_BUCKET')
    return '\n'.join([
        (f'<img src="https://s3.amazonaws.com'
         f'/{deploy_bucket}/{x}" width="50%">')

        for x in s3fn_vec])


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
    assert deploy_bucket

def convert_local_images_to_s3_assets(content_file_path, absolute_asset_dir):
    """
    Args:
        content_file: the html or md file
        absolute_asset_dir: prepend to what is in the <img src=""> right now,
            to convert its relative path to find the image
    """
    output_lines = []
    lines = Path(content_file_path).read_text().split()
    asset_dir = Path(absolute_asset_dir)
    images = []

    # first pass
    for line in lines:
        match = re.search(r"<img\s+src=\"([^\"]+)\"", line)
        relative_path = match.groups()[0]
        absolute_path = asset_dir
        local_path = Path("assets/2022-08-28T012206_1661649829702_0.png")
        image_path = asset_dir / local_path
        assert image_path.exists()
        images.append(image_path)

    print("Ok cool now we know all the images exist. Going to upload,", 
            [x.name for x in images])


def do():
    parser = argparse.ArgumentParser()

    [parser.add_argument(*x[0], **x[1])
            for x in bake_options()]

    # Collect args from user.
    args = vars(parser.parse_args())
    images = [x.replace('\\', '').strip() for x in args.get('images').split(',')]
    print('images', images)
    dry_run = args.get('dry_run')
    title = args.get('title')
    date = args.get('date')
    existing_file = args.get('existing_file')
    out_dir = args.get('out_dir')
    assert existing_file or out_dir

    print(args)
    if existing_file:
        prefix = os.path.basename(existing_file)
        if prefix.endswith('.md'):
            prefix = prefix[:-3]
    else:
        prefix = make_prefix(date=date, title=title)
    print('prefix', prefix)
    check_env_vars()
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
    
    
do()
