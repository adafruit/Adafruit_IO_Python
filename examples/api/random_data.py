"""
'random_data.py'
================================================
Example for accessing the Adafruit IO Random
Data Service.

Author(s): Brent Rubell for Adafruit Industries
"""
# Import standard python modules
import json
import os
# Import Adafruit IO REST client.
from Adafruit_IO import Client

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME', 'YOUR_IO_USERNAME')

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure **not** to publish it when you publish this code!
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY', 'YOUR_IO_KEY')

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

generator_id = 1461

# Get the specified randomizer record with its current value and related details.
random_data = aio.receive_random(generator_id)
# Parse the API response
data = json.dumps(random_data)
data = json.loads(data)
print('Random Data: {0}'.format(data['value']))
