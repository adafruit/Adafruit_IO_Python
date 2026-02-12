"""
'weather.py'
================================================
Dark Sky Hyperlocal for IO Plus
with Adafruit IO API

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
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY', 'YOUR_IO_PASSWORD')

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Grab the weather JSON
weather = aio.receive_weather(1234)
weather = json.dumps(weather)
forecast = json.loads(weather)

# Parse the current forecast
current = forecast['current']
print('Current Forecast')
print('It is {0} and {1}.'.format(current['summary'], current['temperature']))

# Parse the two day forecast
forecast_days_2 = forecast['forecast_days_2']
print('\nWeather in Two Days')
print('It will be {0} with a high of {1}F and a low of {2}F.'.format(
            forecast_days_2['summary'], forecast_days_2['temperatureLow'], forecast_days_2['temperatureHigh']))

# Parse the five day forecast
forecast_days_5 = forecast['forecast_days_5']
print('\nWeather in Five Days')
print('It will be {0} with a high of {1}F and a low of {2}F.'.format(
            forecast_days_5['summary'], forecast_days_5['temperatureLow'], forecast_days_5['temperatureHigh']))