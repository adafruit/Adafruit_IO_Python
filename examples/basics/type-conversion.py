"""
`type-conversion.py`
=========================================
Example of sending and receiving
different data types to/from Adafruit
IO using the Adafruit IO Python Client

Author(s): Brent Rubell, Todd Treece for Adafruit Industries
"""

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'type' feed
    type = aio.feeds('type')
except RequestError: # create a type feed
    feed = Feed(name="type")
    type = aio.create_feed(feed)

# Values to send to Adafruit IO
char_val = 'a'
string_val = 'adafruit'
bool_val = True
int_val = 3
long_val = 0x80000000
double_val = 3.1415926535897932
float_val = +1E6


"""
Let's send some values to our feed
and properly receive them
"""
print("Sending to Adafruit IO...")

# Char
print('\tSending Character: ', char_val)
aio.send(type.key, char_val)
data = aio.receive(type.key).value
print('\t\tReceived Character: ', str(data))

# String
print('\n\tSending String: ', string_val)
aio.send(type.key, string_val)
data = aio.receive(type.key).value
print('\t\tReceived String: ', str(data))

# Boolean
print('\n\tSending Bool: ', bool_val)
aio.send(type.key, bool_val)
data = aio.receive(type.key).value
print('\t\tReceived Bool: ', bool(data))

# Integer
print('\n\tSending Int: ', int_val)
aio.send(type.key, int_val)
data = aio.receive(type.key).value
print('\t\tReceived Int: ', int(data))

# Long
print('\n\tSending Long: ', long_val)
aio.send(type.key, long_val)
data = aio.receive(type.key).value
print('\t\tReceived Long: ', int(data))

# Double
print('\n\tSending Double: ', double_val)
aio.send(type.key, double_val)
data = aio.receive(type.key).value
print('\t\tReceived Double: ', float(data))

# Float
print('\n\tSending Float: ', float_val)
aio.send(type.key, float_val)
data = aio.receive(type.key).value
print('\t\tReceived Float: ', float(data))
