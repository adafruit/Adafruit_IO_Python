"""
`time.py`
==========================================
Don't have a RTC handy and need
accurate time measurements?

Let Adafruit IO serve up real-time values
based off your device's IP-address!

Author: Brent Rubell
"""
# Import standard python modules.
import os

# Import Adafruit IO REST client.
from Adafruit_IO import Client

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME', 'YOUR_AIO_USERNAME')

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure **not** to publish it when you publish this code!
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY', 'YOUR_AIO_KEY')

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Get the time from Adafruit IO
time = aio.receive_time()
# Time is returned as a `struct_time`
# https://docs.python.org/3.7/library/time.html#time.struct_time
print(time)