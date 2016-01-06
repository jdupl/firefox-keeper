import subprocess


class WgetHandler():

    def __init__(self, path):
        self.path = path

    def new(self, task):
        url = task[1]

        try:
            subprocess.check_call(['wget', '--directory-prefix', self.path,
                                   '--page-requisites', '--html-extension',
                                   '--convert-links', url])
        except KeyboardInterrupt as e:
            raise e

    def matches(self, url):
        return False
