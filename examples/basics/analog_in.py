"""
'analog_in.py'
==================================
Example of sending analog sensor
values to an Adafruit IO feed.

Author(s): Brent Rubell

Dependencies:
    - Adafruit_Blinka
        (https://github.com/adafruit/Adafruit_Blinka)
    - Adafruit_CircuitPython_MCP3xxx
        (https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx)
"""
# Import standard python modules
import time

# import Adafruit Blinka
import board
import digitalio
import busio

# import Adafruit IO REST client
from Adafruit_IO import Client, Feed, RequestError

# import Adafruit CircuitPython MCP3xxx library
from adafruit_mcp3xxx import adafruit_mcp3xxx

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'
# Create an instance of the REST client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'analog' feed
    analog = aio.feeds('analog')
except RequestError: # create a analog feed
    feed = Feed(name='analog')
    analog = aio.create_feed(feed)

# Create an instance of the `busio.spi` class
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D12)
# create a mcp3008 object
mcp = adafruit_mcp3xxx.MCP3008(spi,cs)

# create an an adc (single-ended) on pin 0
adc_single_ended = adafruit_mcp3xxx.AnalogIn(mcp,0)

while True:
    sensor_data = adc_single_ended.value

    print('Analog Data -> ', sensor_data)
    aio.send(analog.key, sensor_data)

    # avoid timeout from adafruit io
    time.sleep(0.5)
