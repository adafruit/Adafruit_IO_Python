# Base testcase class with functions and state available to all tests.
# Author: Tony DiCola (tdicola@adafruit.com)
import os
import time
import unittest

import Adafruit_IO


class IOTestCase(unittest.TestCase):

    def get_test_key(self):
        """Return the AIO key specified in the ADAFRUIT_IO_KEY environment
        variable, or raise an exception if it doesn't exist.
        """
        key = os.environ.get('ADAFRUIT_IO_KEY', None)
        if key is None:
            raise RuntimeError("ADAFRUIT_IO_KEY environment variable must be " \
              "set with valid Adafruit IO key to run this test!")
        return key
