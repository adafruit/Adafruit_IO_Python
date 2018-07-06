"""
mqtt_time.py
============================================
example of utilizing MQTT time topics to grab 
the time from the Adafruit IO server.

Author: Brent Rubell
"""

# Import standard python modules.
import sys
import time

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('\t Feed {0} received new value: {1}'.format(feed_id, payload))


# Create a SECURE MQTT client instance
# Note: This client will default to secure, an optional parameter can be added
# to make it insecure, comment out the below line
# client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY, secure=False)
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

# time per loop
loop_time = 2

client.loop_background()
while True:
    print('* Subscribing to /time/seconds')
    client.subscribe_time('seconds')
    time.sleep(loop_time)
    print('* Subscribing to /time/millis')
    client.subscribe_time('millis')
    time.sleep(loop_time)
    print('* Subscribing to iso-8601')
    client.subscribe_time('iso')
    time.sleep(loop_time)
