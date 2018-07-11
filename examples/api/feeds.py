# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed
import json

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# List all of your feeds
feeds = aio.feeds()
print(feeds)

# Create a new feed
feed = Feed(name="PythonFeed")
response = aio.create_feed(feed)
print(response)

# List a specific feed
feed = aio.feeds(response.key)
print(feed)


# Delete a feed
aio.delete_feed(response.key)
