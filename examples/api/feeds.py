# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper, Brent Rubell

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed
import json

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# List all of your feeds
print("Obtaining user's feeds...")
feeds = aio.feeds()
print('Feeds: ', feeds)

# Create a new feed
print("Creating new feed...")
feed = Feed(name="PythonFeed")
response = aio.create_feed(feed)
print("New feed: ", response)

# Delete a feed
aio.delete_feed(response.key)

group2 = aio.groups('example')

# Create feed in a group
feed = Feed(name="PythonGroupFeed")
group_key = "example"
groups = aio.groups()
group = groups[group_key] if group_key in groups else aio.create_group(group_key)
print("Creating feed in group %s"%group_key)
response = aio.create_feed(feed, group_key)
print("New feed: ", response)

# Delete a feed within a group
print("Deleting feed within group %s"%group_key)
aio.delete_feed(response.key)