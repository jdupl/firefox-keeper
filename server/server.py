#!/usr/bin/env python3
import json
import multiprocessing as mp

from flask import Flask, request, jsonify


import time

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


def handle(task):
    print('handling ', task)
    time.sleep(5)
    print('done handling ', task)


def safe_handle(queue):
    while True:
        task = queue.get(True)
        try:
            handle(task)
        except Exception as e:
            print("error: {} handling {}".format(e, task))


def setup():
    global queue
    queue = mp.Queue()
    pool = mp.Pool(5, safe_handle, (queue,))
    return app

if __name__ == '__main__':
    setup().run(debug=True)
