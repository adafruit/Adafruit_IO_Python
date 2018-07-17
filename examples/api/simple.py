# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony DiCola

# Import Adafruit IO REST client.
from Adafruit_IO import Client, RequestError, Feed

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Assign a foo feed, if one exists already
try:
    foo = aio.feeds('foo')
except RequestError: # Doesn't exist, create a new feed
    feed = Feed(name="foo")
    foo = aio.create_feed(feed)

# Assign a test feed, if one exists already
try:
    test = aio.feeds('test')
except RequestError: # Doesn't exist, create a new feed
    feed = Feed(name="test")
    test = aio.create_feed(feed)

# Send a value to the feed 'Test'.
aio.send_data(test.key, 42)

# Send a string value 'bar' to the feed 'Foo'.
aio.send_data(foo.key, 'bar')

# Now read the most recent value from the feed 'Test'.  Notice that it comes
# back as a string and should be converted to an int if performing calculations
# on it.
data = aio.receive(test.key)
print('Retrieved value from Test has attributes: {0}'.format(data))
print('Latest value from Test: {0}'.format(data.value))

# Finally read the most revent value from feed 'Foo'.
data = aio.receive(foo.key)
print('Retrieved value from Foo has attributes: {0}'.format(data))
print('Latest value from Foo: {0}'.format(data.value))
