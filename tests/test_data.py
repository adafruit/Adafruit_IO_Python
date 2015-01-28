# Test Data instance from REST client.
# Author: Tony DiCola (tdicola@adafruit.com)
import Adafruit_IO
import base


class TestData(base.IOTestCase):

    def test_data_properties_are_optional(self):
        data = Adafruit_IO.Data(value='foo', feed_id=10)
        self.assertEqual(data.value, 'foo')
        self.assertEqual(data.feed_id, 10)
        self.assertIsNone(data.created_epoch)
        self.assertIsNone(data.created_at)
        self.assertIsNone(data.updated_at)
        self.assertIsNone(data.completed_at)
        self.assertIsNone(data.expiration)
        self.assertIsNone(data.position)
        self.assertIsNone(data.id)

    def test_from_response_ignores_unknown_items(self):
        data = Adafruit_IO.Data.from_response({'value': 'foo', 'feed_id': 10, 'unknown_param': 42})
        self.assertEqual(data.value, 'foo')
        self.assertEqual(data.feed_id, 10)
        self.assertIsNone(data.created_epoch)
        self.assertIsNone(data.created_at)
        self.assertIsNone(data.updated_at)
        self.assertIsNone(data.completed_at)
        self.assertIsNone(data.expiration)
        self.assertIsNone(data.position)
        self.assertIsNone(data.id)
