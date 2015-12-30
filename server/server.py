#!/usr/bin/env python3
import json

from flask import Flask, request, jsonify

app = Flask(__name__)


def read_bookmark(item, parents=[]):
    print(item, parents)


def read(item, parents=[]):
    for k, v in item.items():
        if type(v) is str:
            read_bookmark(v, parents)
        else:
            parents.append(k)
            read(v, parents)
    if len(parents) > 0:
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


def setup():
    return app

if __name__ == '__main__':
    setup().run(debug=True)
