"""
`rgb_led.py`
=======================================================================
Control a RGB LED using
Adafruit IO and Python

Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-color

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Author(s): Brent Rubell for Adafruit Industries
Copyright (c) 2018 Adafruit Industries
Licensed under the MIT license.
All text above must be included in any redistribution.

Dependencies:
    - Adafruit_Blinka
        (https://github.com/adafruit/Adafruit_Blinka)
    - Adafruit_CircuitPython_PCA9685
        (https://github.com/adafruit/Adafruit_CircuitPython_PCA9685)
"""
# import system libraries
import time

# import Adafruit Blinka
from board import SCL, SDA
from busio import I2C

# import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# import Adafruit IO REST client
from Adafruit_IO import Client, Feed, RequestError

# PWM Pins
RED_PIN = 6
GREEN_PIN = 5
BLUE_PIN = 4

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

# Create the I2C bus interface.
i2c_bus = I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)
pca.frequency = 60
prev_color = '#000000'

def map_range(x, in_min, in_max, out_min, out_max):
    """re-maps a number from one range to another."""
    mapped = (x-in_min) * (out_max - out_min) / (in_max-in_min) + out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)

while True:
    # grab the `color` feed
    color_val = aio.receive(color.key)
    if color_val != prev_color:
        # print rgb values and hex value
        print('Received Color: ')
        red = aio.toRed(color_val.value)
        print('\t - R: ', red)
        green = aio.toGreen(color_val.value)
        print('\t - G: ', green)
        blue = aio.toBlue(color_val.value)
        print('\t - B: ', blue)
        print('\t - HEX: ', color_val.value)
        # map color values (0-255) to  16-bit values for the pca
        red = map_range(int(red), 0, 255, 0, 65535)
        green = map_range(int(green), 0, 255, 0, 65535)
        blue = map_range(int(blue), 0, 255, 0, 65535)
        # invert RGB values for common anode LEDs.
        pca.channels[RED_PIN].duty_cycle = 65535 - int(red)
        pca.channels[GREEN_PIN].duty_cycle = 65535 - int(green)
        pca.channels[BLUE_PIN].duty_cycle = 65535 - int(blue)
    prev_color = color_val
    # let's wait a bit so we don't flood adafruit io's servers...
    time.sleep(1)
