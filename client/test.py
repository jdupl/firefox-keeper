import client
import os
import unittest
import json
import lz4


class ReadLZ4TestCase(unittest.TestCase):

    def compress_fixture(self, fixture_lz4_path):
        """
        Compress json fixture with lz4 and with mozilla header
        """
        fixture_json_path = 'fixtures/fixture.json'

        with open(fixture_json_path, mode='rb') as json_file:
            data = json_file.read()
            compressed_data = lz4.compress(data)

            with open(fixture_lz4_path, mode='wb') as lz4_file:
                header = b'mozLz40\0'
                lz4_file.write(header)
                lz4_file.write(compressed_data)

    def test_read_jsonlz4(self):
        path = 'fixtures/fixture.lz4'
        expected = json.loads("{\"test\": \"test\"}")
        self.compress_fixture(path)

        actual = client.read_jsonlz4(path)

        self.assertEqual(expected, actual)

        os.remove(path)


if __name__ == "__main__":
    unittest.main()
