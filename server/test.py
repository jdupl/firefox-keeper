#!/usr/bin/env python3
import server
import unittest


class ReadModFromUrl(unittest.TestCase):

    def test_find_mod_for_url_html_default(self):
        url = 'https://www.google.com'
        server.setup()

        handler = server.find_mod_for_url(url)

        self.assertEqual("handlers.html_default", handler.__name__)

    def test_find_mod_for_url_youtube(self):
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        server.setup()

        handler = server.find_mod_for_url(url)

        self.assertEqual("handlers.youtube", handler.__name__)

    def test_find_mod_for_url_youtube_with_other_params(self):
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=xxxxx'
        server.setup()

        handler = server.find_mod_for_url(url)

        self.assertEqual("handlers.youtube", handler.__name__)

if __name__ == "__main__":
    unittest.main()
