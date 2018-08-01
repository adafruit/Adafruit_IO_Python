"""
`mqtt_shared_feeds.py`
---------------------------------------------------------
Example of reading and writing to a shared  Adafruit IO Feed.

learn.adafruit.com/adafruit-io-basics-feeds/sharing-a-feed

Author: Brent Rubell for Adafruit Industries 2018
"""

# Import standard python modules.
import sys
import time
import random

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Shared IO Feed
# Make sure you have read AND write access to this feed to publish.
IO_FEED = 'SHARED_AIO_FEED_NAME'

# IO Feed Owner's username
IO_FEED_USERNAME = 'SHARED_AIO_FEED_USERNAME'


# Define callback functions which will be called when certain events happen.
def connected(client):
    """Connected function will be called when the client connects.
    """
    client.subscribe(IO_FEED, IO_FEED_USERNAME)

def disconnected(client):
    """Disconnected function will be called when the client disconnects.
    """
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed has a new value.
    The feed_id parameter identifies the feed, and the payload parameter has
    the new value.
    """
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect       =   connected
client.on_disconnect    =   disconnected
client.on_message       =   message

# Connect to the Adafruit IO server.
client.connect()

client.loop_background()
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')

while True:
    value = random.randint(0, 100)
    print('Publishing {0} to {1}.'.format(value, IO_FEED))
    client.publish(IO_FEED, value, IO_FEED_USERNAME)
    time.sleep(10)
