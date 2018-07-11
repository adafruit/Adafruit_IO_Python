"""
`time-topics.py`
====================================
Don't have a RTC handy and need
accurate time measurements?

Let Adafruit IO serve real-time values!

Author: Brent Rubell
"""
# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, Data, RequestError

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

print('---Adafruit IO REST API Time Helpers---')

print('Seconds: aio.receive_time(seconds)')
secs_val = aio.receive_time('seconds')
print('\t' + secs_val)

print('Milliseconds: aio.receive_time(millis)')
ms_val = aio.receive_time('millis')
print('\t' + ms_val)

print('ISO-8601: aio.receive_time(ISO-8601)')
iso_val = aio.receive_time('ISO-8601')
print('\t' + iso_val)