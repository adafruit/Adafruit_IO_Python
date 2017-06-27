# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed
import json

# Set to your Adafruit IO key.
ADAFRUIT_IO_USERNAME = 'YOUR ADAFRUIT IO USERNAME'
ADAFRUIT_IO_KEY = 'YOUR ADAFRUIT IO KEY'

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
