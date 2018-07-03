"""
'adafruitio_06_digital_in.py'
==================================
Example of sending button values
to an Adafruit IO feed.

Author(s): Brent Rubell, Todd Treece
"""
# import python system libraries
import time

# import Adafruit Blinka
from digitalio import DigitalInOut, Direction, Pull
import digitalio
import board

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'digital' feed
    digital = aio.feeds('digital')
except RequestError: # create a digital feed
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)

# button set up
button = digitalio.DigitalInOut(board.D12)
button.direction = Direction.INPUT
button.pull = None
button_current = 0


while True:
    if not button.value:
        button_current = 1
    else:
        button_current = 0

    print('Sending Value to IO: ', button_current)
    aio.send(digital.key, button_current)

    # avoid timeout from adafruit io
    time.sleep(1)
