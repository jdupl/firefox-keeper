#!/usr/bin/env python3
import lz4
import json

def read_jsonlz4(filename):
    with open(filename, mode='rb') as f:
        if f.read(8) != b"mozLz40\0":
            print("Bad firefox jsonlz4 file.")
            return
        raw_data = f.read()
        uncompressed = lz4.decompress(raw_data)
        return json.loads(uncompressed.decode('utf8'))

def recurse(data):
    for c in data:
        if 'title' in c:
            print(c['title'])
        if 'children' in c:
            recurse(c['children'])

filename = "/home/justin/.mozilla/firefox/9shb6xj3.default/bookmarkbackups/bookmarks-2015-12-24_147_rDZlzXqiTshE+lOx9FDMxg==.jsonlz4"

data = read_jsonlz4(filename)
if not data:
    print('Invalid bookmark file')
    exit(1)

for c in data['children']:
    if 'title' in c:
        print(c['title'])
    if 'children' in c:
        recurse(c['children'])
