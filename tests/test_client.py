# Test REST client.
# Author: Tony DiCola (tdicola@adafruit.com)
import time

import Adafruit_IO
import base

# Turn this on to see responses of requests from urllib.
#import logging
#logging.basicConfig(level=logging.DEBUG)

class TestClient(base.IOTestCase):

    # If your IP isn't put on the list of non-throttled IPs, uncomment the
    # function below to waste time between tests to prevent throttling.
    #def tearDown(self):
    #    time.sleep(30.0)

    def test_set_key(self):
        key = "unique_key_id"
        io = Adafruit_IO.Client(key)
        self.assertEqual(key, io.key)

    def test_delete_feed(self):
        io = Adafruit_IO.Client(self.get_test_key())
        io.send('TestFeed', 'foo')  # Make sure a feed called TestFeed exists.
        io.delete_feed('TestFeed')
        self.assertRaises(Adafruit_IO.RequestError, io.receive, 'TestFeed')

    def test_delete_nonexistant_feed_fails(self):
        io = Adafruit_IO.Client(self.get_test_key())
        self.ensure_feed_deleted(io, 'TestFeed')
        self.assertRaises(Adafruit_IO.RequestError, io.delete_feed, 'TestFeed')

    def test_send_and_receive(self):
        io = Adafruit_IO.Client(self.get_test_key())
        self.ensure_feed_deleted(io, 'TestFeed')
        response = io.send('TestFeed', 'foo')
        self.assertEqual(response.value, 'foo')
        data = io.receive('TestFeed')
        self.assertEqual(data.value, 'foo')

    def test_receive_next(self):
        io = Adafruit_IO.Client(self.get_test_key())
        self.ensure_feed_deleted(io, 'TestFeed')
        io.send('TestFeed', 1)
        data = io.receive_next('TestFeed')
        self.assertEqual(int(data.value), 1)

    def test_receive_previous(self):
        io = Adafruit_IO.Client(self.get_test_key())
        self.ensure_feed_deleted(io, 'TestFeed')
        io.send('TestFeed', 1)
        io.receive_next('TestFeed')
        data = io.receive_previous('TestFeed')
        self.assertEqual(int(data.value), 1)

    def test_data_on_feed_returns_all_data(self):
        io = Adafruit_IO.Client(self.get_test_key())
        self.ensure_feed_deleted(io, 'TestFeed')
        io.send('TestFeed', 1)
        io.send('TestFeed', 2)
        result = io.data('TestFeed')
        self.assertEqual(len(result), 2)
        self.assertEqual(int(result[0].value), 1)
        self.assertEqual(int(result[1].value), 2)

    def test_data_on_feed_and_data_id_returns_data(self):
        io = Adafruit_IO.Client(self.get_test_key())
        self.ensure_feed_deleted(io, 'TestFeed')
        data = io.send('TestFeed', 1)
        result = io.data('TestFeed', data.id)
        self.assertEqual(data.id, result.id)
        self.assertEqual(int(data.value), int(result.value))

    def test_create_data(self):
        io = Adafruit_IO.Client(self.get_test_key())
        self.ensure_feed_deleted(io, 'TestFeed')
        io.send('TestFeed', 1)  # Make sure TestFeed exists.
        data = Adafruit_IO.Data(value=42)
        result = io.create_data('TestFeed', data)
        self.assertEqual(int(result.value), 42)
