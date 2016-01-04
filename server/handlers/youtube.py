import re
import os
import subprocess


pattern = re.compile('http[s]?://(?:www\.)?youtube\.com/watch\?v=(.*)')


def new(task):
    url = task[1]
    dest = '/tmp/'

    m = pattern.match(url)
    youtube_id = m.groups()[0].split('&')[0]  # TODO Better regex

    try:
        subprocess.check_call(['youtube-dl', youtube_id, '-o',
                              os.path.join(dest, '%(title)s-%(id)s.%(ext)s')])
    except KeyboardInterrupt as e:
        raise e


def matches(url):
    return pattern.match(url)
