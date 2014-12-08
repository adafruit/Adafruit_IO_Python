import json

from urllib3 import connection_from_url
from urllib import urlencode, quote

#fork of ApiClient Class: https://github.com/shazow/apiclient
class Client(object):
  #BASE_URL = 'http://localhost:3002/'
  BASE_URL = 'https://io.adafruit.com/'

  def __init__(self, key, rate_limit_lock=None):
    self.key = key
    self.rate_limit_lock = rate_limit_lock
    self.connection_pool = self._make_connection_pool(self.BASE_URL)

  def _make_connection_pool(self, url):
    return connection_from_url(url)

  def _compose_url(self, path):
    return self.BASE_URL + path

  def _compose_get_url(self, path, params=None):
    return self.BASE_URL + path + '?' + urlencode(params)

  def _handle_response(self, response):
    return json.loads(response.data)

  def _request(self, method, path, params=None):
    if (method.lower() == "get"):
      url = self._compose_get_url(path, params)
    else:
      url = self._compose_url(path)

    self.rate_limit_lock and self.rate_limit_lock.acquire()
    headers = {"X-AIO-Key": self.key, 'Content-Type':'application/json'}
    if (method.upper() == "GET"):
      r = self.connection_pool.urlopen(method.upper(), url, headers=headers)
    else:
      r = self.connection_pool.urlopen(method.upper(), url, headers=headers, body=json.dumps(params))

    return self._handle_response(r)

  def _get(self, path, **params):
    return self._request('GET', path, params=params)

  def _post(self, path, params):
    return self._request('POST', path, params=params)

  #stream functionality
  def send(self, feed_name, data):
    feed_name = quote(feed_name)
    path = "api/feeds/{}/streams/send".format(feed_name)
    return self._post(path, {'value': data})

  def receive(self, feed_name):
    feed_name = quote(feed_name)
    path = "api/feeds/{}/streams/last".format(feed_name)
    return self._get(path)

  def receive_next(self, feed_name):
    feed_name = quote(feed_name)
    path = "api/feeds/{}/streams/next".format(feed_name)
    return self._get(path)

  def receive_previous(self, feed_name):
    feed_name = quote(feed_name)
    path = "api/feeds/{}/streams/last".format(feed_name)
    return self._get(path)

  def streams(self, feed_id_or_key, stream_id=None):
    if stream_id is None:
      path = "api/feeds/{}/streams".format(feed_id_or_key)
    else:
      path = "api/feeds/{}/streams/{}".format(feed_id_or_key, stream_id)
    return self._get(path)

  def create_stream(self, feed_id_or_key, data):
    path = "api/feeds/{}/streams".format(feed_id_or_key)
    return self._post(path, data)

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
