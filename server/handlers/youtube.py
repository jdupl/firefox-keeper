import re

pattern = re.compile('http[s]?://(www\.)?youtube\.com/watch\?v=(.*)')


def new(task):
    return('youtube')


def matches(url):
    return pattern.match(url)
