"""
'location.py'
==================================
Example of sending location over an
Adafruit IO feed to a Map Dashboard
block

Author(s): Brent Rubell
"""

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create a location feed
try:
    location = aio.feeds('location')
except RequestError:
    feed = Feed(name="location")
    location = aio.create_feed(feed)


# Top Secret Adafruit HQ Location
value = 1
lat = 40.726190
lon = -74.005334
ele = 6 # elevation above sea level (meters)

# Send location data to Adafruit IO
aio.send_location_data(location.key, value, lat, lon, ele)
