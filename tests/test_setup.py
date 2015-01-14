# Test setup of REST client.
# Author: jwcooper
from Adafruit_IO import Client
import base


class TestSetup(base.IOTestCase):
    def test_set_key(self):
        key = "unique_key_id"
        io = Client(key)
        self.assertEqual(key, io.key)
