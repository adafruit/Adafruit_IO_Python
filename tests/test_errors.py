# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import time
import unittest

from Adafruit_IO import Client, RequestError, ThrottlingError
import base


class TestErrors(base.IOTestCase):

    def test_request_error_from_bad_key(self):
        # the test username is possibly blocked / deleted, so gives a different error
        io = Client("test_user", "this is a bad key from a test")
        with self.assertRaises(RequestError) as error_context:
            io.send("TestStream", 42)
        self.assertRegex(error_context.exception.args[0], ".*(that username|invalid API key provided).*")

    @unittest.skip("Throttling test must be run in isolation to prevent other tests from failing.")
    def test_throttling_error_after_6_requests_in_short_period(self):
        io = Client(self.get_test_username(), self.get_test_key())
        try:
            feed_key = [f.key for f in io.feeds() if f.name == "TestStream"][0]
            io.delete_feed(feed_key)
        except ValueError:
            pass
        new_feed = io.create_feed("TestStream")
        with self.assertRaises(ThrottlingError):
            for i in range(60):
                io.send(new_feed.key, 42)
                time.sleep(0.1)  # Small delay to keep from hammering network.
        io.delete_feed(new_feed.key)
