"""
'location.py'
==================================
Example of sending location over an
Adafruit IO feed to a Map Dashboard
block

Author(s): Brent Rubell
"""

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, Data, RequestError
import datetime

# Set to your Adafruit IO key.
ADAFRUIT_IO_USERNAME = 'YOUR_USERNAME'
ADAFRUIT_IO_KEY = 'YOUR_KEY'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# create a location feed
try:
    location = aio.feeds('location')
except RequestError:
    feed = Feed(name="location")
    location = aio.create_feed(feed)


# Adafruit HQ Coordinates
value = 0
lat = 40.726190
lon = -74.005334
ele = 0

# new send_location_data implementation
aio.send_location_data(location.key,value,lat,lon,ele)


# send_batch_data implementation
data_list = [Data(value=0, id='value', 
lat = 40.726190,lon=-74.005334, ele=0)]
aio.send_batch_data(location.key, data_list)

