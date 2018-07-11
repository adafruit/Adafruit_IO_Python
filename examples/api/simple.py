# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony DiCola

# Import Adafruit IO REST client.
from Adafruit_IO import Client

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Send a value to the feed 'Test'.
aio.send_data('Test', 42)

# Send a string value 'bar' to the feed 'Foo'.
aio.send_data('Foo', 'bar')

# Now read the most recent value from the feed 'Test'.  Notice that it comes
# back as a string and should be converted to an int if performing calculations
# on it.
data = aio.receive('Test')
print('Retrieved value from Test has attributes: {0}'.format(data))
print('Latest value from Test: {0}'.format(data.value))

# Finally read the most revent value from feed 'Foo'.
data = aio.receive('Foo')
print('Retrieved value from Foo has attributes: {0}'.format(data))
print('Latest value from Foo: {0}'.format(data.value))
