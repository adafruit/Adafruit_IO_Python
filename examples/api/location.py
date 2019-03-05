"""
'location.py'
==================================
Example of sending metadata
associated with a data point.

Author(s): Brent Rubell
"""

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create a location feed
try:
    location = aio.feeds('location')
except RequestError:
    feed = Feed(name="location")
    location = aio.create_feed(feed)

value = 42
# Set metadata associated with value
metadata = {'lat': 40.726190,
            'lon': -74.005334,
            'ele': -6,
            'created_at': None}

# Send location data to Adafruit IO
aio.send_data(location.key, value, metadata)
