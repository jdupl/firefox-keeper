import re
import os
import subprocess

pattern = re.compile('http[s]?://(?:www\.)?youtube\.com/watch\?v=(.*)')


class YoutubeHandler():

    def __init__(self, path):
        self.path = path

    def new(self, task):
        url = task[1]

        m = pattern.match(url)
        youtube_id = m.groups()[0].split('&')[0]  # TODO Better regex

        try:
            subprocess.check_call(
                ['youtube-dl', youtube_id, '-o', os.path.join(
                    self.path, '%(title)s-%(id)s.%(ext)s')])
        except KeyboardInterrupt as e:
            raise e

    def matches(self, url):
        return pattern.match(url)
