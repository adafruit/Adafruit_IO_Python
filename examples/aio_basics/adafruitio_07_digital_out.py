"""
'adafruitio_07_digital_out.py'
===================================
Example of turning on and off a LED
from the Adafruit IO Python Client

Author(s): Brent Rubell, Todd Treece
"""
# import python system libraries
import time

# import Adafruit Blinka
from digitalio import DigitalInOut, Direction
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

# led set up
led = digitalio.DigitalInOut(board.D5)
led.direction = Direction.OUTPUT

while True:
    data = aio.receive(digital.key)
    if int(data.value) == 1:
        print('received <- ON\n')
    elif int(data.value) == 0:
        print('received <- OFF\n')

    # set the LED to the feed value
    led.value = int(data.value)
    print(led.value)
    # timeout so we dont flood adafruitio with requests
    time.sleep(0.5)
