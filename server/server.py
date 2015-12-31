#!/usr/bin/env python3
import os
import json
import glob
import importlib
import multiprocessing as mp

from flask import Flask, request, jsonify

app = Flask(__name__)


def read_bookmark(*args):
    queue.put((args))


def read(item, parents=[]):
    for k, v in item.items():
        if type(v) is str:
            read_bookmark(k, v, parents)
        else:
            parents.append(k)
            read(v, parents)
            parents.pop()


@app.route('/api', methods=['POST'])
def update():
    req = json.loads(request.get_json())

    if not req or 'profiles' not in req:
        return jsonify({}), 400

    for profile in req['profiles'].values():
        for k, v in profile.items():
            read(v, [k])
    return jsonify({}), 200


def find_mod_for_url(url):
    global queue, handlers
    for handler in handlers.values():
        if handler.matches(url):
            return handler
    return handlers['html_default']


def handle(task):
    handler = find_mod_for_url(task[1])
    print(handler.new(task))


def safe_handle(queue):
    while True:
        task = queue.get(True)
        try:
            handle(task)
        except Exception as e:
            print("error: {} while handling {}".format(e, task))


def setup():
    global queue, handlers

    handlers = {}
    default_handler = None
    mods = filter(os.path.isfile, glob.glob(os.path.join('handlers', '*.py')))

    for mod_path in mods:
        mod_name = os.path.splitext(os.path.split(mod_path)[-1])[0]
        if mod_name == '__init__':
            continue

        print('Found module "%s"' % mod_name)
        handlers[mod_name] = importlib.import_module('handlers.%s' % mod_name)

    queue = mp.Queue()
    pool = mp.Pool(5, safe_handle, (queue,))

    return app

if __name__ == '__main__':
    setup().run(debug=True)
