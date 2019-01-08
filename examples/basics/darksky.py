"""
Example of getting a forecast from Adafruit IO
Note: This functionality is for IO PLUS users ONLY.

Author: Brent Rubell for Adafruit Industries
"""
# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'USER'

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'PASSWORD'


# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

print('Get all weather integration records without their current forecast values.')
records = aio.receive_weather()
print(records)

print('Get the specified weather record with current weather and all available forecast information.')
forecast = aio.receive_weather(2153)
print(forecast)