"""
Example of using the Adafruit IO MQTT Client
for subscribing to the Adafruit IO Weather Service
Note: This feature is avaliable for IO Plus Subscribers ONLY

Author: Brent Rubell for Adafruit Industries
"""

# Import standard python modules.
import sys

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
forecast_tomorrow = 'forecast_days_2'
# Subscribe to forecast in 5 days
forecast_in_5_days = 'forecast_days_5'

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening to forecast: {0}...'.format(forecast_id))
    # Subscribe to changes on the current forecast.
    client.subscribe_weather(forecast_id, forecast_today)

    # Subscribe to changes on tomorrow's forecast.
    client.subscribe_weather(forecast_id, forecast_tomorrow)

    # Subscribe to changes on forecast in 5 days.
    client.subscribe_weather(forecast_id, forecast_in_5_days)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, topic, payload):
    """Message function will be called when any subscribed forecast has an update.
    Weather data is updated at most once every 20 minutes.
    """
    # Raw data from feed
    print(topic)
    print(payload)
    # parse based on topic
    if topic is 'current':
      # Print out today's forecast
      print('Current Forecast: {0}'.format(payload))
    elif topic is 'forecast_days_2':
      # print out tomorrow's forecast
      print('Forecast Tomorrow: {0}'.format(payload))
    elif topic is 'forecast_days_5':
      # print out forecast in 5 days
      print('Forecast in 5 Days: {0}'.format(payload))

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