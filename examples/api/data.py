# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError
import json

# Set to your Adafruit IO key.
ADAFRUIT_IO_USERNAME = 'YOUR ADAFRUIT IO USERNAME'
ADAFRUIT_IO_KEY = 'YOUR ADAFRUIT IO KEY'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
try:
    temperature = aio.feeds('temperature')
except RequestError:
    feed = Feed(name="temperature")
    temperature = aio.create_feed(feed)

#
# Adding data
#

aio.send(temperature.key, 42)
# works the same as send now
aio.append(temperature.key, 42)

#
# Retrieving data
#

data = aio.receive_next(temperature.key)
print(data)

data = aio.receive(temperature.key)
print(data)

data = aio.receive_previous(temperature.key)
print(data)
