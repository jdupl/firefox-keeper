#!/usr/bin/env python3
import lz4
import json
import re
import os
import glob
import configparser
import requests

from os.path import expanduser


def read_jsonlz4(filename):
    """
    Read mozilla jsonlz4 file

    Returns json
    """
    with open(filename, mode='rb') as f:
        # Check for the mozilla lz4 header
        if f.read(8) != b'mozLz40\0':
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


def read_profile(profile_path):
    bookmark_backup_path = os.path.join(profile_path, 'bookmarkbackups')

    files = filter(os.path.isfile, glob.glob(os.path.join(bookmark_backup_path,
                                                          '*.jsonlz4')))
    files = [os.path.join(bookmark_backup_path, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    if len(files) < 0:
        return

    data = read_jsonlz4(files[0])
    if not data:
        print('Invalid bookmark file')
        return

    bookmarks = {}
    for c in data['children']:
        if 'title' in c and c['title'] != '' and 'children' in c:
            bookmarks[c['title']] = recurse(c['children'])
    return bookmarks

if __name__ == '__main__':
    bookmarks = {}
    http_p = re.compile('^http[s]?://')
    profile_p = re.compile('^Profile[0-9]+')

    config = configparser.ConfigParser()
    config.read(os.path.join(expanduser("~"), '.mozilla/firefox/profiles.ini'))

    for section in config.sections():
        if profile_p.match(section) and 'path' in config[section]:
            bookmarks[section] = read_profile(os.path.join(
                expanduser("~"), '.mozilla/firefox/', config[section]['path']))

    r = requests.post("http://localhost:5000/api",
                      json=json.dumps({'profiles': bookmarks}))
    print(r)
