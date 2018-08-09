"""
`servo.py`
========================================================================

Control a servo with Adafruit IO
Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-servo

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
    - Adafruit_CircuitPython_Motor
        (https://github.com/adafruit/Adafruit_CircuitPython_Motor)
"""

# import system libraries
import time

# import Adafruit Blinka
from board import SCL, SDA
from busio import I2C

# import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# import the adafruit_motor library
from adafruit_motor import servo

# import Adafruit IO REST client
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'servo' feed
    servo_feed = aio.feeds('servo')
except RequestError: # create a servo feed
    feed = Feed(name='servo')
    servo_feed = aio.create_feed(feed)

# Create the I2C bus interface.
i2c_bus = I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 50hz.
pca.frequency = 50
SERVO_CHANNEL = 0

# counter variable for the last servo angle
prev_angle = 0

# set up the servo on PCA channel 0
my_servo = servo.Servo(pca.channels[SERVO_CHANNEL])


while True:
    # grab the `servo` feed value
    servo_angle = aio.receive(servo_feed.key)
    if servo_angle.value != prev_angle:
        print('received <- ', servo_angle.value, 'Degrees')
        # write the servo to the feed-specified angle
        my_servo.angle = int(servo_angle.value)
    prev_angle = servo_angle.value
    # timeout so we don't flood IO with requests
    time.sleep(0.5)
