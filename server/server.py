#!/usr/bin/env python3
import os
import json
import glob
import importlib
import inspect

from queue import Queue
from threading import Thread
from flask import Flask, request, jsonify

app = Flask(__name__)


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        no_interrupt = True
        while no_interrupt:
            task = self.tasks.get(True)
            try:
                handle(task)
            except KeyboardInterrupt:
                no_interrupt = False
            except Exception as e:
                print("error: {} while handling {}".format(e, task))


class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, task):
        self.tasks.put(task)


def read_bookmark(*args):
    pool.add_task((args))


def read(item, parents=[]):
    for k, v in item.items():
        if type(v) is str:
            read_bookmark(k, v, parents)
        else:
            parents.append(k)
            read(v, parents)
            parents.pop()


def find_mod_for_url(url):
    """
    Return handler according to url

    url:
    Url used to match the correct handler

    return:
    The handler
    """
    for handler in handlers.values():
        if handler.matches(url):
            return handler
    return handlers['html_default']


def handle(task):
    handler = find_mod_for_url(task[1])
    try:
        handler.new(task)
    except KeyboardInterrupt as e:
        raise e


@app.route('/api', methods=['POST'])
def update():
    req = json.loads(request.get_json())

    if not req or 'profiles' not in req:
        return jsonify({}), 400

    for profile in req['profiles'].values():
        for k, v in profile.items():
            read(v, [k])
    return jsonify({}), 200


def setup(config_env=None):
    global handlers, pool, app
    app.config.from_pyfile('config/config.cfg')

    if config_env:
        app.config.from_pyfile('config/config.%s.cfg' % config_env, silent=True)

    handlers = {}
    mods = filter(os.path.isfile, glob.glob(os.path.join('handlers', '*.py')))

    for mod_path in mods:
        mod_name = os.path.splitext(os.path.split(mod_path)[-1])[0]
        mod = importlib.import_module('handlers.%s' % mod_name)
        members = inspect.getmembers(mod, inspect.isclass)

        if len(members) != 1:
            continue

        handlers[mod_name] = members[0][1](app.config['ARCHIVE_PATH'])
        print('Found module "%s"' % members[0][0])

    pool = ThreadPool(5)
    return app

if __name__ == '__main__':
    setup('dev').run(debug=True)
