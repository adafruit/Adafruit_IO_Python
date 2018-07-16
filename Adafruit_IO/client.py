# Copyright (c) 2018 Adafruit Industries
# Authors: Justin Cooper & Tony DiCola

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
import json
import pkg_resources
import platform
# import logging

import requests

from .errors import RequestError, ThrottlingError
from .model import Data, Feed, Group

# set outgoing version, pulled from setup.py
version = pkg_resources.require("Adafruit_IO")[0].version
default_headers = {
    'User-Agent': 'AdafruitIO-Python/{0} ({1}, {2} {3})'.format(version,
                                                                platform.platform(),
                                                                platform.python_implementation(),
                                                                platform.python_version())
}

class Client(object):
    """Client instance for interacting with the Adafruit IO service using its
    REST API.  Use this client class to send, receive, and enumerate feed data.
    """

    def __init__(self, username, key, proxies=None, base_url='https://io.adafruit.com', api_version = 'v2'):
        """Create an instance of the Adafruit IO REST API client.  Key must be
        provided and set to your Adafruit IO access key value.  Optionaly
        provide a proxies dict in the format used by the requests library, a
        base_url to point at a different Adafruit IO service (the default is
        the production Adafruit IO service over SSL), and a api_version to
        add support for future API versions.
        """
        self.username = username
        self.key = key
        self.proxies = proxies
        self.api_version = api_version
        # self.logger = logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        # Save URL without trailing slash as it will be added later when
        # constructing the path.
        self.base_url = base_url.rstrip('/')

    def _compose_url(self, path, is_time=None):
        if not is_time:
            return '{0}/api/{1}/{2}/{3}'.format(self.base_url, self.api_version, self.username, path)
        else: # return a call to https://io.adafruit.com/api/v2/time/{unit}
            return '{0}/api/{1}/{2}'.format(self.base_url, self.api_version, path)


    def _handle_error(self, response):
        # Throttling Error
        if response.status_code == 429:
            raise ThrottlingError()
        # Resource on AdafruitIO not Found Error
        elif response.status_code == 400:
            raise RequestError(response)
        # Handle all other errors (400 & 500 level HTTP responses)
        elif response.status_code >= 400:
            raise RequestError(response)
        # Else do nothing if there was no error.

    def _headers(self, given):
        headers = default_headers.copy()
        headers.update(given)
        return headers

    def _get(self, path, is_time=None):
        response = requests.get(self._compose_url(path, is_time),
                                headers=self._headers({'X-AIO-Key': self.key}),
                                proxies=self.proxies)
        self._handle_error(response)
        if not is_time:
            return response.json()
        else: # time doesn't need to serialize into json, just return text
            return response.text

    def _post(self, path, data):
        response = requests.post(self._compose_url(path),
                                 headers=self._headers({'X-AIO-Key': self.key,
                                                        'Content-Type': 'application/json'}),
                                 proxies=self.proxies,
                                 data=json.dumps(data))
        self._handle_error(response)
        return response.json()

    def _delete(self, path):
        response = requests.delete(self._compose_url(path),
                                   headers=self._headers({'X-AIO-Key': self.key,
                                            'Content-Type': 'application/json'}),
                                   proxies=self.proxies)
        self._handle_error(response)

    # Data functionality.
    def send_data(self, feed, value):
        """Helper function to simplify adding a value to a feed.  Will append the
        specified value to the feed identified by either name, key, or ID.
        Returns a Data instance with details about the newly appended row of data.
        Note that send_data now operates the same as append.
        """
        return self.create_data(feed, Data(value=value))

    send = send_data

    def send_batch_data(self, feed, data_list):
        """Create a new row of data in the specified feed.  Feed can be a feed
        ID, feed key, or feed name.  Data must be an instance of the Data class
        with at least a value property set on it.  Returns a Data instance with
        details about the newly appended row of data.
        """
        path = "feeds/{0}/data/batch".format(feed)
        data_dict = type(data_list)((data._asdict() for data in data_list))
        self._post(path, {"data": data_dict})

    def append(self, feed, value):
        """Helper function to simplify adding a value to a feed.  Will append the
        specified value to the feed identified by either name, key, or ID.
        Returns a Data instance with details about the newly appended row of data.
        Note that unlike send the feed should exist before calling append.
        """
        return self.create_data(feed, Data(value=value))

    def send_location_data(self, feed, value, lat, lon, ele):
        """Sends locational data to a feed

        args:
            - lat: latitude 
            - lon: logitude
            - ele: elevation
            - (optional) value: value to send to the feed
        """
        return self.create_data(feed, Data(value = value,lat=lat, lon=lon, ele=ele))

    def receive_time(self, time):
        """Returns the time from the Adafruit IO server.

        args:
            - time (string): millis, seconds, ISO-8601
        """
        timepath = "time/{0}".format(time)
        return self._get(timepath, is_time=True)

    def receive(self, feed):
        """Retrieve the most recent value for the specified feed.  Feed can be a
        feed ID, feed key, or feed name.  Returns a Data instance whose value
        property holds the retrieved value.
        """
        path = "feeds/{0}/data/last".format(feed)
        return Data.from_dict(self._get(path))

    def receive_next(self, feed):
        """Retrieve the next unread value from the specified feed.  Feed can be
        a feed ID, feed key, or feed name.  Returns a Data instance whose value
        property holds the retrieved value.
        """
        path = "feeds/{0}/data/next".format(feed)
        return Data.from_dict(self._get(path))

    def receive_previous(self, feed):
        """Retrieve the previous unread value from the specified feed.  Feed can
        be a feed ID, feed key, or feed name.  Returns a Data instance whose
        value property holds the retrieved value.
        """
        path = "feeds/{0}/data/previous".format(feed)
        return Data.from_dict(self._get(path))

    def data(self, feed, data_id=None):
        """Retrieve data from a feed.  Feed can be a feed ID, feed key, or feed
        name.  Data_id is an optional id for a single data value to retrieve.
        If data_id is not specified then all the data for the feed will be
        returned in an array.
        """
        if data_id is None:
            path = "feeds/{0}/data".format(feed)
            return list(map(Data.from_dict, self._get(path)))
        else:
            path = "feeds/{0}/data/{1}".format(feed, data_id)
            return Data.from_dict(self._get(path))

    def create_data(self, feed, data):
        """Create a new row of data in the specified feed.  Feed can be a feed
        ID, feed key, or feed name.  Data must be an instance of the Data class
        with at least a value property set on it.  Returns a Data instance with
        details about the newly appended row of data.
        """
        path = "feeds/{0}/data".format(feed)
        return Data.from_dict(self._post(path, data._asdict()))

    def delete(self, feed, data_id):
        """Delete data from a feed.  Feed can be a feed ID, feed key, or feed
        name.  Data_id must be the ID of the piece of data to delete.
        """
        path = "feeds/{0}/data/{1}".format(feed, data_id)
        self._delete(path)

    # Feed functionality.
    def feeds(self, feed=None):
        """Retrieve a list of all feeds, or the specified feed.  If feed is not
        specified a list of all feeds will be returned.  If feed is specified it
        can be a feed name, key, or ID and the requested feed will be returned.
        """
        if feed is None:
            path = "feeds"
            return list(map(Feed.from_dict, self._get(path)))
        else:
            path = "feeds/{0}".format(feed)
            return Feed.from_dict(self._get(path))

    def create_feed(self, feed):
        """Create the specified feed.  Feed should be an instance of the Feed
        type with at least the name property set.
        """
        path = "feeds/"
        return Feed.from_dict(self._post(path, {"feed": feed._asdict()}))

    def delete_feed(self, feed):
        """Delete the specified feed.  Feed can be a feed ID, feed key, or feed
        name.
        """
        path = "feeds/{0}".format(feed)
        self._delete(path)

    def receive_group(self, group):
        """Retrieve the most recent value for the specified group.  Group can be
        a group ID, group key, or group name.  Returns a Group instance whose
        feeds property holds an array of Feed instances associated with the group.
        """
        path = "groups/{0}/last".format(group)
        return Group.from_dict(self._get(path))

    def receive_next_group(self, group):
        """Retrieve the next unread value from the specified group.  Group can
        be a group ID, group key, or group name.  Returns a Group instance whose
        feeds property holds an array of Feed instances associated with the
        group.
        """
        path = "groups/{0}/next".format(group)
        return Group.from_dict(self._get(path))

    def receive_previous_group(self, group):
        """Retrieve the previous unread value from the specified group.  Group
        can be a group ID, group key, or group name.  Returns a Group instance
        whose feeds property holds an array of Feed instances associated with
        the group.
        """
        path = "groups/{0}/previous".format(group)
        return Group.from_dict(self._get(path))

    def groups(self, group=None):
        """Retrieve a list of all groups, or the specified group.  If group is
        not specified a list of all groups will be returned.  If group is
        specified it can be a group name, key, or ID and the requested group
        will be returned.
        """
        if group is None:
            path = "groups/"
            return list(map(Group.from_dict, self._get(path)))
        else:
            path = "groups/{0}".format(group)
            return Group.from_dict(self._get(path))

    def create_group(self, group):
        """Create the specified group.  Group should be an instance of the Group
        type with at least the name and feeds property set.
        """
        path = "groups/"
        return Group.from_dict(self._post(path, group._asdict()))

    def delete_group(self, group):
        """Delete the specified group.  Group can be a group ID, group key, or
        group name.
        """
        path = "groups/{0}".format(group)
        self._delete(path)
