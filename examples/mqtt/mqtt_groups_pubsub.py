# Example of subscribing to an Adafruit IO group
# and publishing to the feeds within it

# Author: Brent Rubell for Adafruit Industries, 2018

# Import standard python modules.
import random
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

# Group Name
group_name = 'grouptest'

# Feeds within the group
group_feed_one = 'one'
group_feed_two = 'two'

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to topic changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Listening for changes on ', group_name)
    # Subscribe to changes on a group, `group_name`
    client.subscribe_group(group_name)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, topic_id, payload):
    # Message function will be called when a subscribed topic has a new value.
    # The topic_id parameter identifies the topic, and the payload parameter has
    # the new value.
    print('Topic {0} received new value: {1}'.format(topic_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()
# Now send new values every 5 seconds.
print('Publishing a new message every 5 seconds (press Ctrl-C to quit)...')
while True:
    value = random.randint(0, 100)
    print('Publishing {0} to {1}.{2}.'.format(value, group_name, group_feed_one))
    client.publish('one', value, group_name)

    value = random.randint(0,100)
    print('Publishing {0} to {1}.{2}.'.format(value, group_name, group_feed_two))
    client.publish('two', value, group_name)
    time.sleep(5)
