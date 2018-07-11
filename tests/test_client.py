# Test REST client.
# Author: Tony DiCola (tdicola@adafruit.com)
import time
import unittest

from Adafruit_IO import Client, Data, Feed, Group, RequestError

import base


# Default config for tests to run against real Adafruit IO service with no proxy.
BASE_URL  = 'https://io.adafruit.com/'
PROXIES   = None

# Config to run tests against real Adafruit IO service over non-SSL and with a
# a proxy running on localhost 8888 (good for getting traces with fiddler).
#BASE_URL  = 'http://io.adafruit.vm/'
#PROXIES   = {'http': 'http://localhost:8888/'}


class TestClient(base.IOTestCase):

    # If your IP isn't put on the list of non-throttled IPs, uncomment the
    # function below to waste time between tests to prevent throttling.
    #def tearDown(self):
    #    time.sleep(30.0)

    # Helper Methods
    def get_client(self):
        # Construct an Adafruit IO REST client and return it.
        return Client(self.get_test_username(), self.get_test_key(), proxies=PROXIES, base_url=BASE_URL, api_version = "v2")

    def ensure_feed_deleted(self, client, feed):
        # Delete the specified feed if it exists.
        try:
            client.delete_feed(feed)
        except RequestError:
            # Swallow the error if the feed doesn't exist.
            pass

    def ensure_group_deleted(self, client, group):
        # Delete the specified group if it exists.
        try:
            client.delete_group(group)
        except RequestError:
            # Swallow the error if the group doesn't exist.
            pass

    def empty_feed(self, client, feed):
        # Remove all the data from a specified feed (but don't delete the feed).
        data = client.data(feed)
        for d in data:
            client.delete(feed, d.id)

    # Test Adafruit IO Key Functionality
    def test_set_key_and_username(self):
        username = "unique_username"
        key = "unique_key_id"
        io = Client(username, key)
        self.assertEqual(username, io.username)
        self.assertEqual(key, io.key)

    # Test Data Functionality
    def test_send_and_receive(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        test_feed = io.create_feed(Feed(name="testfeed"))
        response = io.send_data('testfeed', 'foo')
        self.assertEqual(response.value, 'foo')
        data = io.receive('testfeed')
        self.assertEqual(data.value, 'foo')

    def test_send_batch_data(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        test_feed = io.create_feed(Feed(name="testfeed"))
        data_list = [Data(value=42), Data(value=42)]
        io.send_batch_data(test_feed.key, data_list)
        data = io.receive(test_feed.key)
        self.assertEqual(int(data.value), 42)

    def test_receive_next(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        test_feed = io.create_feed(Feed(name="testfeed"))
        io.send_data('testfeed', 1)
        data = io.receive_next('testfeed')
        self.assertEqual(int(data.value), 1)

    def test_receive_previous(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        test_feed = io.create_feed(Feed(name="testfeed"))
        io.send_data(test_feed.key, 1)
        io.receive_next(test_feed.key)  # Receive 1
        data = io.receive_previous(test_feed.key)
        self.assertEqual(int(data.value), 1)
        io.send_data(test_feed.key, 2)
        io.receive_next(test_feed.key)  # Receive 2
        data = io.receive_previous(test_feed.key)
        self.assertEqual(int(data.value), 2)

    def test_data_on_feed_returns_all_data(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        test_feed = io.create_feed(Feed(name="testfeed"))
        io.send_data('testfeed', 1)
        io.send_data('testfeed', 2)
        result = io.data('testfeed')
        self.assertEqual(len(result), 2)
        self.assertEqual(int(result[0].value), 2)
        self.assertEqual(int(result[1].value), 1)

    def test_data_on_feed_and_data_id_returns_data(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        test_feed = io.create_feed(Feed(name="testfeed"))
        data = io.send_data('testfeed', 1)
        result = io.data('testfeed', data.id)
        self.assertEqual(data.id, result.id)
        self.assertEqual(int(data.value), int(result.value))

    def test_create_data(self):
        aio = self.get_client()
        self.ensure_feed_deleted(aio, 'testfeed')
        test_feed = aio.create_feed(Feed(name="testfeed"))
        aio.send_data('testfeed', 1)  # Make sure TestFeed exists.
        data = Data(value=42)
        result = aio.create_data('testfeed', data)
        self.assertEqual(int(result.value), 42)
    
    def test_location_data(self):
        aio = self.get_client()
        self.ensure_feed_deleted(aio, 'testlocfeed')
        test_feed = aio.create_feed(Feed(name="testlocfeed"))
        aio.send_location_data(test_feed.key, 0, 40, -74, 6)
        data = aio.receive(test_feed.key)
        self.assertEqual(int(data.value), 0)
        self.assertEqual(float(data.lat), 40.0)
        self.assertEqual(float(data.lon), -74.0)
        self.assertEqual(float(data.ele), 6.0)


    # Test Feed Functionality
    def test_append_by_feed_name(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        feed = io.create_feed(Feed(name='testfeed'))
        result = io.append('testfeed', 42)
        self.assertEqual(int(result.value), 42)

    def test_append_by_feed_key(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        feed = io.create_feed(Feed(name='testfeed'))
        result = io.append(feed.key, 42)
        self.assertEqual(int(result.value), 42)

    def test_create_feed(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        feed = Feed(name='testfeed')
        result = io.create_feed(feed)
        self.assertEqual(result.name, 'testfeed')

    def test_feeds_returns_all_feeds(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        feed = io.create_feed(Feed(name='testfeed'))
        io.send_data('testfeed', 1)  # Make sure TestFeed exists.
        feeds = io.feeds()
        self.assertGreaterEqual(len(feeds), 1)
        names = set(map(lambda x: x.name, feeds))
        self.assertTrue('testfeed' in names)

    def test_feeds_returns_requested_feed(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        feed = io.create_feed(Feed(name='testfeed'))
        io.send_data('testfeed', 1)  # Make sure TestFeed exists.
        result = io.feeds('testfeed')
        self.assertEqual(result.name, 'testfeed')

    def test_delete_feed(self):
        io = self.get_client()
        io.send_data('testfeed', 'foo')  # Make sure a feed called TestFeed exists.
        io.delete_feed('testfeed')
        self.assertRaises(RequestError, io.receive, 'testfeed')

    def test_delete_nonexistant_feed_fails(self):
        io = self.get_client()
        self.ensure_feed_deleted(io, 'testfeed')
        self.assertRaises(RequestError, io.delete_feed, 'testfeed')


    # Test Group Functionality
    def test_groups_returns_all_groups(self):
        io = self.get_client()
        groups = io.groups()
        self.assertGreaterEqual(len(groups), 1)
        names = set(map(lambda x: x.name, groups))
        self.assertTrue('grouptest' in names)

    def test_groups_retrieves_requested_group(self):
        io = self.get_client()
        self.ensure_group_deleted(io, 'grouptest')
        response = io.create_group(Group(name='grouptest'))
        self.assertEqual(response.name, 'grouptest')
        self.assertEqual(response.key, 'grouptest')

    def test_delete_group(self):
        io = self.get_client()
        self.ensure_group_deleted(io, 'groupdeletetest')
        group = io.create_group(Group(name='groupdeletetest'))
        io.delete_group('groupdeletetest')
        self.assertRaises(RequestError, io.groups, 'groupdeletetest')

    def test_receive_group_by_name(self):
        io = self.get_client()
        self.ensure_group_deleted(io, 'grouprx')
        group = io.create_group(Group(name='grouprx'))
        response = io.groups(group.name)
        self.assertEqual(response.name, 'grouprx')

    def test_receive_group_by_key(self):
        io = self.get_client()
        self.ensure_group_deleted(io, 'grouprx')
        group = io.create_group(Group(name='grouprx'))
        response = io.groups(group.key)
        self.assertEqual(response.key, 'grouprx')
