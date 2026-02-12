"""
'digital_out.py'
===================================
Example of turning on and off a LED
from the Adafruit IO Python Client

Author(s): Brent Rubell, Todd Treece
"""

# Import standard python modules
import time

# import Adafruit Blinka
import digitalio
import board

# import Adafruit IO REST client.
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

try:  # if we have a 'digital' feed
    digital = aio.feeds("digital")
except RequestError:  # create a digital feed
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)

# led set up
led = digitalio.DigitalInOut(board.D5)
led.direction = digitalio.Direction.OUTPUT


while True:
    TIME_TO_SLEEP = 0.5
    try:
        data = aio.receive(digital.key)
        if int(data.value) == 1:
            print("received <- ON\n")
        elif int(data.value) == 0:
            print("received <- OFF\n")

        # set the LED to the feed value
        led.value = int(data.value)

    except RequestError as e:
        # feed with no data will return 404
        if "not found" in str(e).lower():
            print(
                "Feed 'digital' has no data yet!\n"
                + "Try adding some at https://io.adafruit.com/{0}/feeds/digital".format(
                    ADAFRUIT_IO_USERNAME
                )
            )
            TIME_TO_SLEEP = 5  # allow a few seconds for user to add some data
        else:
            print("Error retrieving data from feed 'digital': {0}".format(e))
    # timeout so we dont flood adafruit-io with requests
    time.sleep(TIME_TO_SLEEP)
