import collections
import json

from urllib3 import connection_from_url
from urllib import urlencode, quote


class AdafruitIOError(Exception):
  """Base class for all Adafruit IO request failures."""
  pass


class RequestError(Exception):
  """General error for a failed Adafruit IO request."""
  def __init__(self, response):
    super(RequestError, self).__init__("Adafruit IO request failed: {0} {1}".format(
      response.status, response.reason))


class ThrottlingError(AdafruitIOError):
  """Too many requests have been made to Adafruit IO in a short period of time.
  Reduce the rate of requests and try again later.
  """
  def __init__(self):
    super(ThrottlingError, self).__init__("Exceeded the limit of Adafruit IO "  \
      "requests in a short period of time. Please reduce the rate of requests " \
      "and try again later.")


class Data(collections.namedtuple('Data', ['created_epoch', 'created_at',
  'updated_at', 'value', 'completed_at', 'feed_id', 'expiration', 'position',
  'id'])):
  """Row of data from a feed.  This is a simple class that just represents data
  returned from the Adafruit IO service.  The value property has the value of the
  data row, and other properties like created_at or id represent the metadata
  of the data row.
  """
  
  @classmethod
  def from_response(cls, response):
    """Create a new Data instance based on the response dict from an Adafruit IO
    request.
    """
    # Be careful to support forward compatibility by only looking at attributes
    # which this Data class knows about (i.e. ignore anything else that's
    # unknown).
    # In this case iterate through all the fields of the named tuple and grab
    # their value from the response dict.  If any field doesn't exist in the
    # response dict then set it to None.
    return cls(*[response.get(x, None) for x in cls._fields])

# Magic incantation to make all parameters to the constructor optional with a
# default value of None.  This is useful when creating an explicit Data instance
# to pass to create_data with only the value or other properties set.
Data.__new__.__defaults__ = tuple(None for x in Data._fields)


#fork of ApiClient Class: https://github.com/shazow/apiclient
class Client(object):
  """Client instance for interacting with the Adafruit IO service using its REST
  API.  Use this client class to send, receive, and enumerate feed data.
  """
  BASE_URL = 'https://io.adafruit.com/'

  def __init__(self, key, rate_limit_lock=None):
    """Create an instance of the Adafruit IO REST API client.  Key must be
    provided and set to your Adafruit IO access key value.
    """
    self.key = key
    self.rate_limit_lock = rate_limit_lock
    self.connection_pool = self._make_connection_pool(self.BASE_URL)

  def _make_connection_pool(self, url):
    return connection_from_url(url)

  def _compose_url(self, path):
    return self.BASE_URL + path

  def _compose_get_url(self, path, params=None):
    return self.BASE_URL + path + '?' + urlencode(params)

  def _handle_error(sefl, response):
    # Handle explicit errors.
    if response.status == 429:
      raise ThrottlingError()
    # Handle all other errors (400 & 500 level HTTP responses)
    elif response.status >= 400:
      raise RequestError(response)
    # Else do nothing if there was no error.

  def _handle_response(self, response, expect_result):
    self._handle_error(response)
    if expect_result:
      return json.loads(response.data)
    # Else no result expected so just return.

  def _request(self, method, path, params=None, expect_result=True):
    if (method.lower() == "get"):
      url = self._compose_get_url(path, params)
    else:
      url = self._compose_url(path)

    self.rate_limit_lock and self.rate_limit_lock.acquire()
    headers = {"X-AIO-Key": self.key, 'Content-Type':'application/json'}
    if (method.upper() == "GET"):
      r = self.connection_pool.urlopen(method.upper(), url, headers=headers)
    else:
      r = self.connection_pool.urlopen(method.upper(), url, headers=headers,
                                       body=json.dumps(params))

    return self._handle_response(r, expect_result)

  def _get(self, path, **params):
    return self._request('GET', path, params=params)

  def _post(self, path, params):
    return self._request('POST', path, params=params)

  def _delete(self, path):
    return self._request('DELETE', path, expect_result=False)

  #feed functionality
  def delete_feed(self, feed):
    """Delete the specified feed.  Feed can be a feed ID, feed key, or feed name.
    """
    feed = quote(feed)
    path = "api/feeds/{}".format(feed)
    self._delete(path)

  #feed data functionality
  def send(self, feed_name, value):
    """Helper function to simplify adding a value to a feed.  Will find the 
    specified feed by name or create a new feed if it doesn't exist, then will
    append the provided value to the feed.  Returns a Data instance with details
    about the newly appended row of data.
    """
    feed_name = quote(feed_name)
    path = "api/feeds/{}/data/send".format(feed_name)
    return Data.from_response(self._post(path, {'value': value}))

  def receive(self, feed):
    """Retrieve the most recent value for the specified feed.  Feed can be a
    feed ID, feed key, or feed name.  Returns a Data instance whose value
    property holds the retrieved value.
    """
    feed = quote(feed)
    path = "api/feeds/{}/data/last".format(feed)
    return Data.from_response(self._get(path))

  def receive_next(self, feed):
    """Retrieve the next unread value from the specified feed.  Feed can be a
    feed ID, feed key, or feed name.  Returns a Data instance whose value
    property holds the retrieved value.
    """
    feed = quote(feed)
    path = "api/feeds/{}/data/next".format(feed)
    return Data.from_response(self._get(path))

  def receive_previous(self, feed):
    """Retrieve the previously read value from the specified feed.  Feed can be
    a feed ID, feed key, or feed name.  Returns a Data instance whose value
    property holds the retrieved value.
    """
    feed = quote(feed)
    path = "api/feeds/{}/data/last".format(feed)
    return Data.from_response(self._get(path))

  def data(self, feed, data_id=None):
    """Retrieve data from a feed.  Feed can be a feed ID, feed key, or feed name.
    Data_id is an optional id for a single data value to retrieve.  If data_id
    is not specified then all the data for the feed will be returned in an array.
    """
    if data_id is None:
      path = "api/feeds/{}/data".format(feed)
      return map(Data.from_response, self._get(path))
    else:
      path = "api/feeds/{}/data/{}".format(feed, data_id)
      return Data.from_response(self._get(path))

  def create_data(self, feed, data):
    """Create a new row of data in the specified feed.  Feed can be a feed ID,
    feed key, or feed name.  Data must be an instance of the Data class with at
    least a value property set on it.  Returns a Data instance with details
    about the newly appended row of data.
    """
    path = "api/feeds/{}/data".format(feed)
    return Data.from_response(self._post(path, data._asdict()))

  #group functionality
  def send_group(self, group_name, data):
    group_name = quote(group_name)
    path = "api/groups/{}/send".format(group_name)
    return self._post(path, {'value': data})

  def receive_group(self, group_name):
    group_name = quote(group_name)
    path = "api/groups/{}/last".format(group_name)
    return self._get(path)

  def receive_next_group(self, group_name):
    group_name = quote(group_name)
    path = "api/groups/{}/next".format(group_name)
    return self._get(path)

  def receive_previous_group(self, group_name):
    group_name = quote(group_name)
    path = "api/groups/{}/last".format(group_name)
    return self._get(path)

  def groups(self, group_id_or_key):
    path = "api/groups/{}".format(group_id_or_key)
    return self._get(path)

  def create_group(self, group_id_or_key, data):
    path = "api/groups/{}".format(group_id_or_key)
    return self._post(path, data)
