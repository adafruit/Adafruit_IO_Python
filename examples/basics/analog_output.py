"""
`analog_output.py`
===============================================================================
PWM a LED from Adafruit IO!

Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-analog-output

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

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_IO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_IO_USERNAME'

# Create the I2C bus interface.
i2c_bus = I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)
PCA_CHANNEL = 4

# Set the PWM frequency to 60hz.
pca.frequency = 60
prev_read = 0

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'analog' feed
    analog = aio.feeds('analog')
except RequestError: # create an `analog` feed
    feed = Feed(name='analog')
    analog = aio.create_feed(feed)


def map_range(x, in_min, in_max, out_min, out_max):
    """re-maps a number from one range to another."""
    mapped = (x-in_min) * (out_max - out_min) / (in_max-in_min) + out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)

while True:
    # grab the `analog` feed value
    analog_read = aio.receive(analog.key)
    if analog_read.value != prev_read:
        print('received <- ', analog_read.value)
        # map the analog value from 0 - 1023 to 0 - 65534
        analog_value = map_range(int(analog_read.value), 0, 1024, 0, 65534)
        # set the LED to the mapped feed value
        pca.channels[PCA_CHANNEL].duty_cycle = int(analog_value)
    prev_read = analog_read.value
    # timeout so we don't flood IO with requests
    time.sleep(0.5)
