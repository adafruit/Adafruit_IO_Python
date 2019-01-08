"""
Example of using the Adafruit IO MQTT Client
for subscribing to the Adafruit IO Weather Service
Note: This feature is avaliable for IO Plus Subscribers ONLY

API Documentation: https://io.adafruit.com/services/weather

Author: Brent Rubell for Adafruit Industries
"""

# Import standard python modules.
import sys
import json

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'USER'

# Set to ID of the forecast to subscribe to for updates
forecast_id = 2153

# Set to the ID of the feed to subscribe to for updates.
"""
Valid forecast types are:
current
forecast_minutes_5
forecast_minutes_30
forecast_hours_1
forecast_hours_2
forecast_hours_6
forecast_hours_24
forecast_days_1
forecast_days_2
forecast_days_5
"""
# Subscribe to the current forecast
forecast_today = 'current'
# Subscribe to tomorrow's forecast
forecast_two_days = 'forecast_days_2'
# Subscribe to forecast in 5 days
forecast_in_5_days = 'forecast_days_5'

# Define callback functions which will be called when certain events happen.
# pylint: disable=redefined-outer-name
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening to forecast: {0}...'.format(forecast_id))
    # Subscribe to changes on the current forecast.
    client.subscribe_weather(forecast_id, forecast_today)

    # Subscribe to changes on tomorrow's forecast.
    client.subscribe_weather(forecast_id, forecast_two_days)

    # Subscribe to changes on forecast in 5 days.
    client.subscribe_weather(forecast_id, forecast_in_5_days)

# pylint: disable=unused-argument
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

# pylint: disable=unused-argument
def message(client, topic, payload):
    """Message function will be called when any subscribed forecast has an update.
    Weather data is updated at most once every 20 minutes.
    """
    # forecast based on mqtt topic
    if topic == 'current':
        # Print out today's forecast
        today_forecast = payload
        print('\nCurrent Forecast')
        parseForecast(today_forecast)
    elif topic == 'forecast_days_2':
        # Print out tomorrow's forecast
        two_day_forecast = payload
        print('\nWeather in Two Days')
        parseForecast(two_day_forecast)
    elif topic == 'forecast_days_5':
        # Print out forecast in 5 days
        five_day_forecast = payload
        print('\nWeather in 5 Days')
        parseForecast(five_day_forecast)

def parseForecast(forecast_data):
    """Parses and prints incoming forecast data
    """
    # incoming data is a utf-8 string, encode it as a json object
    forecast = json.loads(forecast_data)
    # Print out the forecast
    try:
        print('It is {0} and {1}F.'.format(forecast['summary'], forecast['temperature']))
    except KeyError:
        # future weather forecasts return a high and low temperature, instead of 'temperature'
        print('It will be {0} with a high of {1}F and a low of {2}F.'.format(
            forecast['summary'], forecast['temperatureLow'], forecast['temperatureHigh']))
    print('with humidity of {0}%, wind speed of {1}mph, and {2}% chance of precipitation.'.format(
        forecast['humidity'], forecast['windSpeed'], forecast['precipProbability']))

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_blocking()
