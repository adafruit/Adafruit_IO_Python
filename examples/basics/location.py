"""
'location.py'
====================================
Example of sending GPS data points
to an Adafruit IO Feed using the API

Author(s): Brent Rubell, Todd Treece
"""
# Import standard python modules
import time

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

# Assign a location feed, if one exists already
try:
    location = aio.feeds('location')
except RequestError: # Doesn't exist, create a new feed
    feed = Feed(name="location")
    location = aio.create_feed(feed)

# limit feed updates to every 3 seconds, avoid IO throttle
loop_delay = 5

# We dont' have a GPS hooked up, but let's fake it for the example/test:
# (replace this data with values from a GPS hardware module)
value = 0
lat = 40.726190
lon = -74.005334
ele = 6 # elevation above sea level (meters)


while True:
    print('\nSending Values to location feed...\n')
    print('\tValue: ', value)
    print('\tLat: ', lat)
    print('\tLon: ', lon)
    print('\tEle: ', ele)
    # Send location data to Adafruit IO
    aio.send_location_data(location.key, value, lat, lon, ele)
    # shift all values (for test/demo purposes)
    value += 1
    lat -= 0.01
    lon += -0.02
    ele += 1

    # Read the location data back from IO
    print('\nData Received by Adafruit IO Feed:\n')
    data = aio.receive(location.key)
    print('\tValue: {0}\n\tLat: {1}\n\tLon: {2}\n\tEle: {3}'
          .format(data.value, data.lat, data.lon, data.ele))
    # wait loop_delay seconds to avoid api throttle
    time.sleep(loop_delay)
