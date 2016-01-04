import server
import os
import unittest


class ReadModFromUrl(unittest.TestCase):

    def test_find_mod_for_url_html_default(self):
        url = 'https://www.google.com'
        server.setup()

        handler = server.find_mod_for_url(url)

        self.assertEqual("handlers.html_default", handler.__name__)


if __name__ == "__main__":
    unittest.main()
