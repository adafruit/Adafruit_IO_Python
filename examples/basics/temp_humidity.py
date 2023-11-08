"""
'temp_humidity.py'
==================================
Example of sending temperature and humidity data to Adafruit IO

Author(s): Brent Rubell

Tutorial Link: Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-temperature-and-humidity

Dependencies:
    - Adafruit IO Python Client
        (https://github.com/adafruit/io-client-python)
    - Adafruit_CircuitPython_AHTx0
        (https://github.com/adafruit/Adafruit_CircuitPython_AHTx0)
"""

# import standard python modules.
import time

# import adafruit-blinka modules
import board

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Import AHTx0 library
import adafruit_ahtx0

# Set true to send tempertaure data in degrees fahrenheit ('f')?
USE_DEGREES_F = False

# Time between sensor reads, in seconds
READ_TIMEOUT = 60

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username).
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Assign a temperature feed, if one exists already
try:
    temperature_feed = aio.feeds('temperature')
except RequestError: # Doesn't exist, create a new feed
    feed_temp = Feed(name="temperature")
    temperature_feed = aio.create_feed(feed_temp)

# Assign a humidity feed, if one exists already
try:
    humidity_feed = aio.feeds('humidity')
except RequestError: # Doesn't exist, create a new feed
    feed_humid = Feed(name="humidity")
    humidity_feed = aio.create_feed(feed_humid)

# Initialize the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# Initialize AHT20 using the default address (0x38) and the board's default i2c bus
sensor = adafruit_ahtx0.AHTx0(i2c)

while True:
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    if USE_DEGREES_F:
        temperature = temperature * 9.0 / 5.0 + 32.0
        print('Temp={0:0.1f}*F'.format(temperature))
    else:
        print('Temp={0:0.1f}*C'.format(temperature))
    print('Humidity={1:0.1f}%'.format(humidity))
    # Format sensor data as string for sending to Adafruit IO
    temperature = '%.2f'%(temperature)
    humidity = '%.2f'%(humidity)
    # Send humidity and temperature data to Adafruit IO
    aio.send(temperature_feed.key, str(temperature))
    aio.send(humidity_feed.key, str(humidity))

    # Timeout to avoid flooding Adafruit IO
    time.sleep(READ_TIMEOUT)
