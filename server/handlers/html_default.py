import subprocess


def new(task):
    dest = '/tmp'
    url = task[1]

    try:
        subprocess.check_call(['wget', '--directory-prefix', dest,
                               '--page-requisites', '--html-extension',
                               '--convert-links', url])
    except KeyboardInterrupt as e:
        raise e


def matches(url):
    return False
