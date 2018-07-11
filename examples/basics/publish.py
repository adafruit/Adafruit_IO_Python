"""
'publish.py'
=========================================
Publishes an incrementing value to a feed

Author(s): Brent Rubell, Todd Treece for Adafruit Industries
"""
# Import standard python modules
import time

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed

# holds the count for the feed
run_count = 0

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create a new feed named 'counter'
feed = Feed(name="Counter")
response = aio.create_feed(feed)


while True:
    print('sending count: ', run_count)
    run_count += 1
    aio.send_data('counter', run_count)
    # Adafruit IO is rate-limited for publishing
    # so we'll need a delay for calls to aio.send_data()
    time.sleep(3)
