"""
'random_data.py'
================================================
Example for accessing the Adafruit IO Random
Data Service.

Author(s): Brent Rubell for Adafruit Industries
"""
# Import JSON for forecast parsing
import json
# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
ADAFRUIT_IO_USERNAME = 'brubell'
ADAFRUIT_IO_KEY = '6ec4b31bd2c54a09be911e0c1909b7ab'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

generator_id = 1461

# Get the specified randomizer record with its current value and related details.
random_data = aio.receive_random(generator_id)
# Parse the API response
data = json.dumps(random_data)
data = json.loads(data)
print('Random Data: {0}'.format(data['value']))