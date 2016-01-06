#!/usr/bin/env python3
import server
import unittest


class ReadModFromUrl(unittest.TestCase):

    def test_find_mod_for_url_html_default(self):
        url = 'https://www.google.com'
        server.setup()

        handler = server.find_mod_for_url(url)

        self.assertEqual("WgetHandler", handler.__class__.__name__)

    def test_find_mod_for_url_youtube(self):
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        server.setup()

        handler = server.find_mod_for_url(url)

        self.assertEqual("YoutubeHandler", handler.__class__.__name__)

    def test_find_mod_for_url_youtube_with_other_params(self):
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=xxxxx'
        server.setup()

        handler = server.find_mod_for_url(url)

        self.assertEqual("YoutubeHandler", handler.__class__.__name__)

if __name__ == "__main__":
    unittest.main()
