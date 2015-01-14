# Test error responses with REST client.
# Author: Tony DiCola (tdicola@adafruit.com)
import time
import unittest

import Adafruit_IO
import base


class TestErrors(base.IOTestCase):

    def test_request_error_from_bad_key(self):
        io = Adafruit_IO.Client("this is a bad key from a test")
        with self.assertRaises(Adafruit_IO.RequestError):
            io.send("TestStream", 42)

    @unittest.skip("Throttling test must be run in isolation to prevent other failures.")
    def test_throttling_error_after_6_requests_in_short_period(self):
        io = Adafruit_IO.Client(self.get_test_key())
        with self.assertRaises(Adafruit_IO.ThrottlingError):
            for i in range(6):
                io.send("TestStream", 42)
                time.sleep(0.1)  # Small delay to keep from hammering network.
