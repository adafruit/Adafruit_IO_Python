"""
'adafruitio_06_digital_in.py'
==================================
Example of sending GPS data points 
to an Adafruit IO Feed using the API

Author(s): Brent Rubell, Todd Treece
"""
# import python system libraries
import time

# import Adafruit Blinka
from digitalio import DigitalInOut, Direction, Pull
from board import *

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
ADAFRUIT_IO_USERNAME = 'user'
ADAFRUIT_IO_KEY = 'key
'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try:
    digital = aio.feeds('digital')
except RequestError:
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)

# button set up
button = digitalio.DigitalInOut(board.D5)
button.direction = Direction.INPUT
button.pull = Pull.UP

while True:
    if button.value:
        print('ON, sending button...\n')
        aio.send(digital.key, 0)
    else:
        print('OFF, sending button..\n')
        aio.send(digital.key, 1)
    
    # avoid timeout from adafruit io
    time.sleep(0.01)