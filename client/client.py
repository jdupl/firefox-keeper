#!/usr/bin/env python3
import lz4
import json
import re


def read_jsonlz4(filename):
    with open(filename, mode='rb') as f:
        if f.read(8) != b"mozLz40\0":
            return
        raw_data = f.read()
        uncompressed = lz4.decompress(raw_data)
        return json.loads(uncompressed.decode('utf8'))


def recurse(data):
    bookmarks = {}
    for c in data:
        if 'title' in c:
            if 'uri' not in c and 'children' in c:
                bookmarks[c['title']] = recurse(c['children'])
            elif 'uri' in c and http_p.match(c['uri']):
                bookmarks[c['title']] = c['uri']
    return bookmarks


http_p = re.compile('^http[s]?://')
filename = "/home/justin/.mozilla/firefox/9shb6xj3.default/bookmarkbackups/bookmarks-2015-12-24_147_rDZlzXqiTshE+lOx9FDMxg==.jsonlz4"

data = read_jsonlz4(filename)
if not data:
    print('Invalid bookmark file')
    exit(1)

bookmarks = {}
for c in data['children']:
    if 'title' in c and c['title'] != '' and 'children' in c:
        bookmarks[c['title']] = recurse(c['children'])
print(json.dumps(bookmarks))
