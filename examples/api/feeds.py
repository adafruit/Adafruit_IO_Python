# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper, Brent Rubell, Tyeth Gundry

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
print("Obtaining user's feeds (key, name)...")
feeds = aio.feeds()
print([(f.key, f.name) for f in feeds])
print("End of feeds listing.\n")

# Create a new feed
print("Creating new feed...")
feed = Feed(name="PythonFeed")
response = aio.create_feed(feed)
print("New feed: ", response)

# Delete a feed
print("Deleting feed...", end="")
aio.delete_feed(response.key)
print("done.\n")

# Get / Create group - use aio.groups(key) and catch the error or do this:
GROUP_KEY = "example"
groups = aio.groups()
group_keys = [g.key for g in groups]
group = (
    groups[group_keys.index(GROUP_KEY)]
    if GROUP_KEY in group_keys
    else aio.create_group(GROUP_KEY)
)

# Create feed in a group
feed = Feed(name="PythonGroupFeed")
print("Creating feed in group %s" % GROUP_KEY)
response = aio.create_feed(feed, GROUP_KEY)
print("New feed: ", response)

# Delete a feed within a group
print("Deleting feed within group %s..." % GROUP_KEY, end="")
aio.delete_feed(response.key)
print("done.")
