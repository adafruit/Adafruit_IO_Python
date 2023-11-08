"""
`rgb_led.py`
=======================================================================
Control a NeoPixel RGB LED using Adafruit IO and Python

Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-color

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Author(s): Brent Rubell for Adafruit Industries
Copyright (c) 2023 Adafruit Industries
Licensed under the MIT license.
All text above must be included in any redistribution.

Dependencies:
    - Adafruit_Blinka
        (https://github.com/adafruit/Adafruit_Blinka)
    - Adafruit_CircuitPython_NeoPixel
        (https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel)
"""
import time
import board
import neopixel
from Adafruit_IO import Client, Feed, RequestError

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 1

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'color' feed
    color = aio.feeds('color')
except RequestError: # create an `color` feed
    feed = Feed(name='color')
    color = aio.create_feed(feed)

while True:
    # get the value of the Adafruit IO `color` feed
    color_val = aio.receive(color.key)
    # Print hex value
    print('Received Color HEX: ', color_val)
    pixels.fill(color_val.value)
    pixels.show()

    # let's sleep/wait so we don't flood adafruit io's servers with requests
    time.sleep(3)
