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
from collections import namedtuple


# List of fields/properties that are present on a data object from IO.
DATA_FIELDS   = [ 'created_epoch',
                  'created_at',
                  'updated_at',
                  'value',
                  'completed_at',
                  'feed_id',
                  'expiration',
                  'position',
                  'id',
                  'lat',
                  'lon',
                  'ele']

FEED_FIELDS   = [ 'name',
                  'key',
                  'id',
                  'description',
                  'unit_type',
                  'unit_symbol',
                  'history',
                  'visibility',
                  'license',
                  'status_notify',
                  'status_timeout']

GROUP_FIELDS  = [ 'description',
                  'source_keys',
                  'id',
                  'source',
                  'key',
                  'feeds',
                  'properties',
                  'name' ]

DASHBOARD_FIELDS   = [ 'name',
                       'key',
                       'description',
                       'show_header',
                       'color_mode',
                       'block_borders',
                       'header_image_url',
                       'blocks' ]

BLOCK_FIELDS  = [ 'name',
                  'id',
                  'visual_type',
                  'properties',
                  'block_feeds' ]

LAYOUT_FIELDS  = ['xl',
                  'lg',
                  'md',
                  'sm',
                  'xs' ]

# These are very simple data model classes that are based on namedtuple.  This is
# to keep the classes simple and prevent any confusion around updating data
# locally and forgetting to send those updates back up to the IO service (since
# tuples are immutable you can't change them!).  Depending on how people use the
# client it might be prudent to revisit this decision and consider making these
# full fledged classes that are mutable.
Data   = namedtuple('Data', DATA_FIELDS)
Feed   = namedtuple('Feed', FEED_FIELDS)
Group  = namedtuple('Group', GROUP_FIELDS)
Dashboard = namedtuple('Dashboard', DASHBOARD_FIELDS)
Block  = namedtuple('Block', BLOCK_FIELDS)
Layout = namedtuple('Layout', LAYOUT_FIELDS)

# Magic incantation to make all parameters to the initializers optional with a
# default value of None.
Group.__new__.__defaults__  = tuple(None for x in GROUP_FIELDS)
Data.__new__.__defaults__   = tuple(None for x in DATA_FIELDS)
Layout.__new__.__defaults__   = tuple(None for x in LAYOUT_FIELDS)

# explicitly set dashboard values so that 'color_mode' is 'dark'
Dashboard.__new__.__defaults__ = (None, None, None, False, "dark", True, None, None)

# explicitly set block values so 'properties' is a dictionary
Block.__new__.__defaults__ = (None, None, None, {}, None)

# explicitly set feed values
Feed.__new__.__defaults__ = (None, None, None, None, None, None, 'ON', 'Private', None, None, None)

# Define methods to convert from dicts to the data types.
def _from_dict(cls, data):
    # Convert dict to call to class initializer (to work with the data types
    # base on namedtuple).  However be very careful to preserve forwards
    # compatibility by ignoring any attributes in the dict which are unknown
    # by the data type.
    params = {x: data.get(x, None) for x in cls._fields}
    return cls(**params)


def _feed_from_dict(cls, data):
    params = {x: data.get(x, None) for x in cls._fields}
    return cls(**params)


def _group_from_dict(cls, data):
    params = {x: data.get(x, None) for x in cls._fields}
    # Parse the feeds if they're provided and generate feed instances.
    params['feeds'] = tuple(map(Feed.from_dict, data.get('feeds', [])))
    return cls(**params)


def _dashboard_from_dict(cls, data):
    params = {x: data.get(x, None) for x in cls._fields}
    # Parse the blocks if they're provided and generate block instances.
    params['blocks'] = tuple(map(Block.from_dict, data.get('blocks', [])))
    return cls(**params)


# Now add the from_dict class methods defined above to the data types.
Data.from_dict   = classmethod(_from_dict)
Feed.from_dict   = classmethod(_feed_from_dict)
Group.from_dict  = classmethod(_group_from_dict)
Dashboard.from_dict  = classmethod(_dashboard_from_dict)
Block.from_dict  = classmethod(_from_dict)
Layout.from_dict  = classmethod(_from_dict)
