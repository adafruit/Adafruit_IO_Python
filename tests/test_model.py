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
from Adafruit_IO import Data, Feed, Group, Dashboard, Block, Layout, GroupFeedData

import base


class TestData(base.IOTestCase):

    def test_data_properties_are_optional(self):
        """Data fields have optional properties
        """
        data = Data(value='foo', feed_id=10)
        self.assertEqual(data.value, 'foo')
        self.assertEqual(data.feed_id, 10)
        self.assertIsNone(data.created_epoch)
        self.assertIsNone(data.created_at)
        self.assertIsNone(data.updated_at)
        self.assertIsNone(data.completed_at)
        self.assertIsNone(data.expiration)
        self.assertIsNone(data.position)
        self.assertIsNone(data.id)
        self.assertIsNone(data.lat)
        self.assertIsNone(data.lon)
        self.assertIsNone(data.ele)


    def test_feeds_have_explicitly_set_values(self):
        """ Let's make sure feeds are explicitly set from within the model:
        Feed.__new__.__defaults__ = (None, None, None, None, None, None, 'ON', 'Private', None, None, None)
        """
        feed = Feed(name='foo')
        self.assertEqual(feed.name, 'foo')
        self.assertIsNone(feed.key)
        self.assertIsNone(feed.id)
        self.assertIsNone(feed.description)
        self.assertIsNone(feed.unit_type)
        self.assertIsNone(feed.unit_symbol)
        self.assertEqual(feed.history, 'ON')
        self.assertEqual(feed.visibility, 'Private')
        self.assertIsNone(feed.license)
        self.assertIsNone(feed.status_notify)
        self.assertIsNone(feed.status_timeout)

    def test_group_properties_are_optional(self):
        group = Group(name="foo")
        self.assertEqual(group.name, 'foo')
        self.assertIsNone(group.description)
        self.assertIsNone(group.source_keys)
        self.assertIsNone(group.id)
        self.assertIsNone(group.key)
        self.assertIsNone(group.feeds)
        self.assertIsNone(group.properties)

        """ Let's make sure feeds are explicitly set from within the model:
        Dashboard.__new__.__defaults__ = (None, None, None, False, "dark", True, None, None)

        """
    def test_dashboard_have_explicitly_set_values(self):
        dashboard = Dashboard(name="foo")
        self.assertEqual(dashboard.name, 'foo')
        self.assertIsNone(dashboard.key)
        self.assertIsNone(dashboard.description)
        self.assertFalse(dashboard.show_header)
        self.assertEqual(dashboard.color_mode, 'dark')
        self.assertTrue(dashboard.block_borders)
        self.assertIsNone(dashboard.header_image_url)
        self.assertIsNone(dashboard.blocks)

        """ Let's make sure feeds are explicitly set from within the model:
        Block.__new__.__defaults__ = (None, None, None {}, None)
        """
    def test_block_have_explicitly_set_values(self):
        block = Block(name="foo")
        self.assertEqual(block.name, 'foo')
        self.assertIsNone(block.id)
        self.assertIsNone(block.visual_type)
        self.assertEqual(type(block.properties), dict)
        self.assertEqual(len(block.properties), 0)
        self.assertIsNone(block.block_feeds)

    def test_layout_properties_are_optional(self):
        layout = Layout()
        self.assertIsNone(layout.xl)
        self.assertIsNone(layout.lg)
        self.assertIsNone(layout.md)
        self.assertIsNone(layout.sm)
        self.assertIsNone(layout.xs)

    def test_from_dict_ignores_unknown_items(self):
        data = Data.from_dict({'value': 'foo', 'feed_id': 10, 'unknown_param': 42})
        self.assertEqual(data.value, 'foo')
        self.assertEqual(data.feed_id, 10)
        self.assertIsNone(data.created_epoch)
        self.assertIsNone(data.created_at)
        self.assertIsNone(data.updated_at)
        self.assertIsNone(data.completed_at)
        self.assertIsNone(data.expiration)
        self.assertIsNone(data.position)
        self.assertIsNone(data.id)


class TestGroupFeedData(base.IOTestCase):

    def test_groupfeeddata_properties_are_optional(self):
        """GroupFeedData fields have optional properties
        """
        data = GroupFeedData(value='foo', key='test_key')
        self.assertEqual(data.value, 'foo')
        self.assertEqual(data.key, 'test_key')

    def test_groupfeeddata_from_dict_ignores_unknown_items(self):
        data = GroupFeedData.from_dict({'value': 'foo', 'key': 'test_key', 'unknown_param': 42})
        self.assertEqual(data.value, 'foo')
        self.assertEqual(data.key, 'test_key')
        self.assertFalse(hasattr(data, 'unknown_param'))
