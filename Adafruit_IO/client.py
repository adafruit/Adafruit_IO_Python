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
import time
from time import struct_time
import json
import platform
import pkg_resources
import re
from urllib.parse import urlparse
from urllib.parse import parse_qs
# import logging

import requests

from .errors import RequestError, ThrottlingError
from .model import Data, Feed, Group, Dashboard, Block, Layout

DEFAULT_PAGE_LIMIT = 100

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

    def __init__(self, username, key, proxies=None, base_url='https://io.adafruit.com'):
        """Create an instance of the Adafruit IO REST API client.  Key must be
        provided and set to your Adafruit IO access key value.  Optionaly
        provide a proxies dict in the format used by the requests library,
        and a base_url to point at a different Adafruit IO service
        (the default is the production Adafruit IO service over SSL).
        """
        self.username = username
        self.key = key
        self.proxies = proxies
        # self.logger = logging.basicConfig(level=logging.DEBUG,
        #                                   format='%(asctime)s - %(levelname)s - %(message)s')

        # Save URL without trailing slash as it will be added later when
        # constructing the path.
        self.base_url = base_url.rstrip('/')

        # Store the last response of a get or post
        self._last_response = None

    @staticmethod
    def to_red(data):
        """Hex color feed to red channel.
        
        :param int data: Color value, in hexadecimal.
        """
        return ((int(data[1], 16))*16) + int(data[2], 16)

    @staticmethod
    def to_green(data):
        """Hex color feed to green channel.

        :param int data: Color value, in hexadecimal.
        """
        return (int(data[3], 16) * 16) + int(data[4], 16)

    @staticmethod
    def to_blue(data):
        """Hex color feed to blue channel.

        :param int data: Color value, in hexadecimal.
        """
        return (int(data[5], 16) * 16) + int(data[6], 16)

    @staticmethod
    def _headers(given):
        headers = default_headers.copy()
        headers.update(given)
        return headers

    @staticmethod
    def _create_payload(value, metadata):
        if metadata is not None:
            payload = Data(value=value, lat=metadata['lat'], lon=metadata['lon'],
                           ele=metadata['ele'], created_at=metadata['created_at'])
            return payload
        return Data(value=value)

    @staticmethod
    def _handle_error(response):
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

    def _compose_url(self, path):
        return '{0}/api/{1}/{2}/{3}'.format(self.base_url, 'v2', self.username, path)

    def _get(self, path, params=None):
        response = requests.get(self._compose_url(path),
                                headers=self._headers({'X-AIO-Key': self.key}),
                                proxies=self.proxies,
                                params=params)
        self._last_response = response
        self._handle_error(response)
        return response.json()

    def _post(self, path, data):
        response = requests.post(self._compose_url(path),
                                 headers=self._headers({'X-AIO-Key': self.key,
                                                        'Content-Type': 'application/json'}),
                                 proxies=self.proxies,
                                 data=json.dumps(data))
        self._last_response = response
        self._handle_error(response)
        return response.json()

    def _delete(self, path):
        response = requests.delete(self._compose_url(path),
                                   headers=self._headers({'X-AIO-Key': self.key,
                                                          'Content-Type': 'application/json'}),
                                   proxies=self.proxies)
        self._last_response = response
        self._handle_error(response)

    # Data functionality.
    def send_data(self, feed, value, metadata=None, precision=None):
        """Helper function to simplify adding a value to a feed.  Will append the
        specified value to the feed identified by either name, key, or ID.
        Returns a Data instance with details about the newly appended row of data.
        Note that send_data now operates the same as append.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        :param string value: Value to send.
        :param dict metadata: Optional metadata associated with the value.
        :param int precision: Optional amount of precision points to send.
        """
        if precision:
            try:
                value = round(value, precision)
            except NotImplementedError:
                raise NotImplementedError("Using the precision kwarg requires a float value")
        payload = self._create_payload(value, metadata)
        return self.create_data(feed, payload)

    send = send_data

    def send_batch_data(self, feed, data_list):
        """Create a new row of data in the specified feed.  Feed can be a feed
        ID, feed key, or feed name.  Data must be an instance of the Data class
        with at least a value property set on it.  Returns a Data instance with
        details about the newly appended row of data.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        :param Data data_list: Multiple data values.
        """
        path = "feeds/{0}/data/batch".format(feed)
        data_dict = type(data_list)((data._asdict() for data in data_list))
        self._post(path, {"data": data_dict})

    def append(self, feed, value):
        """Helper function to simplify adding a value to a feed.  Will append the
        specified value to the feed identified by either name, key, or ID.
        Returns a Data instance with details about the newly appended row of data.
        Note that unlike send the feed should exist before calling append.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        :param string value: Value to append to feed.
        """
        return self.create_data(feed, Data(value=value))

    def receive_time(self, timezone=None):
        """Returns a struct_time from the Adafruit IO Server based on requested
        timezone, or automatically based on the device's IP address.
        https://docs.python.org/3.7/library/time.html#time.struct_time

        :param string timezone: Optional timezone to return the time in.
        See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
        """
        path = 'integrations/time/struct.json'
        if timezone:
            path += f'?tz={timezone}'
        return self._parse_time_struct(self._get(path))

    @staticmethod
    def _parse_time_struct(time_dict: dict) -> time.struct_time:
        """Parse the time data returned by the server and return a time_struct

        Corrects for the weekday returned by the server in Sunday=0 format
        (Python expects Monday=0)
        """
        wday = (time_dict['wday'] - 1) % 7
        return struct_time((time_dict['year'], time_dict['mon'], time_dict['mday'],
                            time_dict['hour'], time_dict['min'], time_dict['sec'],
                            wday, time_dict['yday'], time_dict['isdst']))

    def receive_weather(self, weather_id=None):
        """Adafruit IO Weather Service, Powered by Dark Sky

        :param int id: optional ID for retrieving a specified weather record.
        """
        if weather_id:
            weather_path = "integrations/weather/{0}".format(weather_id)
        else:
            weather_path = "integrations/weather"
        return self._get(weather_path)

    def receive_random(self, randomizer_id=None):
        """Access to Adafruit IO's Random Data
        service.

        :param int randomizer_id: optional ID for retrieving a specified randomizer.
        """
        if randomizer_id:
            random_path = "integrations/words/{0}".format(randomizer_id)
        else:
            random_path = "integrations/words"
        return self._get(random_path)

    def receive(self, feed):
        """Retrieve the most recent value for the specified feed. Returns a Data
        instance whose value property holds the retrieved value.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        """
        path = "feeds/{0}/data/last".format(feed)
        return Data.from_dict(self._get(path))

    def receive_next(self, feed):
        """Retrieve the next unread value from the specified feed. Returns a Data
        instance whose value property holds the retrieved value.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        """
        path = "feeds/{0}/data/next".format(feed)
        return Data.from_dict(self._get(path))

    def receive_previous(self, feed):
        """Retrieve the previous unread value from the specified feed. Returns a
        Data instance whose value property holds the retrieved value.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        """
        path = "feeds/{0}/data/previous".format(feed)
        return Data.from_dict(self._get(path))

    def data(self, feed, data_id=None, max_results=DEFAULT_PAGE_LIMIT):
        """Retrieve data from a feed. If data_id is not specified then all the data
        for the feed will be returned in an array.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        :param string data_id: ID of the piece of data to delete.
        :param int max_results: The maximum number of results to return. To
            return all data, set to None.
        """
        if max_results is None:
            res = self._get(f'feeds/{feed}/details')
            max_results = res['details']['data']['count']
        if data_id:
            path = "feeds/{0}/data/{1}".format(feed, data_id)
            return Data.from_dict(self._get(path))

        params = {'limit': max_results} if max_results else None
        data = []
        path = "feeds/{0}/data".format(feed)
        while len(data) < max_results:
            data.extend(list(map(Data.from_dict, self._get(path,
                                                           params=params))))
            nlink = self.get_next_link()
            if not nlink:
                break
            # Parse the link for the query parameters
            params = parse_qs(urlparse(nlink).query)
            if max_results:
                params['limit'] = max_results - len(data)
        return data

    def get_next_link(self):
        """Parse the `next` page URL in the pagination Link header.

        This is necessary because of a bug in the API's implementation of the
        link header. If that bug is fixed, the link would be accesible by
        response.links['next']['url'] and this method would be broken.

        :return: The url for the next page of data
        :rtype: str
        """
        if not self._last_response:
            return
        link_header = self._last_response.headers['link']
        res = re.search('rel="next", <(.+?)>', link_header)
        if not res:
            return
        return res.groups()[0]

    def create_data(self, feed, data):
        """Create a new row of data in the specified feed.
        Returns a Data instance with details about the newly
        appended row of data.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        :param Data data: Instance of the Data class. Must have a value property set.
        """
        path = "feeds/{0}/data".format(feed)
        return Data.from_dict(self._post(path, data._asdict()))

    def delete(self, feed, data_id):
        """Delete data from a feed.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        :param string data_id: ID of the piece of data to delete.
        """
        path = "feeds/{0}/data/{1}".format(feed, data_id)
        self._delete(path)

    # feed functionality.
    def feeds(self, feed=None):
        """Retrieve a list of all feeds, or the specified feed.  If feed is not
        specified a list of all feeds will be returned.

        :param string feed: Name/Key/ID of Adafruit IO feed, defaults to None.
        """
        if feed is None:
            path = "feeds"
            return list(map(Feed.from_dict, self._get(path)))
        path = "feeds/{0}".format(feed)
        return Feed.from_dict(self._get(path))

    def create_feed(self, feed, group_key=None):
        """Create the specified feed.

        :param string feed: Key of Adafruit IO feed.
        :param group_key group: Group to place new feed in.
        """
        f = feed._asdict()
        del f['id']  # Don't pass id on create call
        path = "feeds/"
        if group_key is not None: # create feed in a group
            path="/groups/%s/feeds"%group_key
            return Feed.from_dict(self._post(path, {"feed": f}))
        return Feed.from_dict(self._post(path, {"feed": f}))

    def delete_feed(self, feed):
        """Delete the specified feed.

        :param string feed: Name/Key/ID of Adafruit IO feed.
        """
        path = "feeds/{0}".format(feed)
        self._delete(path)

    # Group functionality.
    def groups(self, group=None):
        """Retrieve a list of all groups, or the specified group.

        :param string group: Name/Key/ID of Adafruit IO Group. Defaults to None.
        """
        if group is None:
            path = "groups/"
            return list(map(Group.from_dict, self._get(path)))
        path = "groups/{0}".format(group)
        return Group.from_dict(self._get(path))

    def create_group(self, group):
        """Create the specified group.

        :param string group: Name/Key/ID of Adafruit IO Group.
        """
        path = "groups/"
        return Group.from_dict(self._post(path, group._asdict()))

    def delete_group(self, group):
        """Delete the specified group.

        :param string group: Name/Key/ID of Adafruit IO Group.
        """
        path = "groups/{0}".format(group)
        self._delete(path)

    # Dashboard functionality.
    def dashboards(self, dashboard=None):
        """Retrieve a list of all dashboards, or the specified dashboard.

        :param string dashboard: Key of Adafruit IO Dashboard. Defaults to None.
        """
        if dashboard is None:
            path = "dashboards/"
            return list(map(Dashboard.from_dict, self._get(path)))
        path = "dashboards/{0}".format(dashboard)
        return Dashboard.from_dict(self._get(path))

    def create_dashboard(self, dashboard):
        """Create the specified dashboard.

        :param Dashboard dashboard: Dashboard object to create
        """
        path = "dashboards/"
        return Dashboard.from_dict(self._post(path, dashboard._asdict()))

    def delete_dashboard(self, dashboard):
        """Delete the specified dashboard.

        :param string dashboard: Key of Adafruit IO Dashboard.
        """
        path = "dashboards/{0}".format(dashboard)
        self._delete(path)

    # Block functionality.
    def blocks(self, dashboard, block=None):
        """Retrieve a list of all blocks from a dashboard, or the specified block.

        :param string dashboard: Key of Adafruit IO Dashboard.
        :param string block: id of Adafruit IO Block. Defaults to None.
        """
        if block is None:
            path = "dashboards/{0}/blocks".format(dashboard)
            return list(map(Block.from_dict, self._get(path)))
        path = "dashboards/{0}/blocks/{1}".format(dashboard, block)
        return Block.from_dict(self._get(path))

    def create_block(self, dashboard, block):
        """Create the specified block under the specified dashboard.

        :param string dashboard: Key of Adafruit IO Dashboard.
        :param Block block: Block object to create under dashboard
        """
        path = "dashboards/{0}/blocks".format(dashboard)
        return Block.from_dict(self._post(path, block._asdict()))

    def delete_block(self, dashboard, block):
        """Delete the specified block.

        :param string dashboard: Key of Adafruit IO Dashboard.
        :param string block: id of Adafruit IO Block.
        """
        path = "dashboards/{0}/blocks/{1}".format(dashboard, block)
        self._delete(path)

    # Layout functionality.
    def layouts(self, dashboard):
        """Retrieve the layouts array from a dashboard

        :param string dashboard: key of Adafruit IO Dashboard.
        """
        path = "dashboards/{0}".format(dashboard)
        dashboard = self._get(path)
        return Layout.from_dict(dashboard['layouts'])

    def update_layout(self, dashboard, layout):
        """Update the layout of the specified dashboard.

        :param string dashboard: Key of Adafruit IO Dashboard.
        :param Layout layout: Layout object to update under dashboard
        """
        path = "dashboards/{0}/update_layouts".format(dashboard)
        return Layout.from_dict(self._post(path, {'layouts': layout._asdict()}))
