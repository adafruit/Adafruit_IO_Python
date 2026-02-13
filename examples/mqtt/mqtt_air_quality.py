"""
Example of using the Adafruit IO MQTT Client
for subscribing to the Adafruit IO Air Quality Service
Note: This feature is avaliable for IO Plus Subscribers ONLY

API Documentation: https://io.adafruit.com/services/air_quality

Author: Brent Rubell for Adafruit Industries
"""
import json
import os
import sys
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME', 'USER')
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY', 'KEY')

# Set to ID of the air quality record to subscribe to for updates
aq_id = 1234

def connected(client):
    print('Connected to Adafruit IO!  Listening for Air Quality changes...')
    # Takes an optional forecast: current, forecast_today, forecast_tomorrow
    client.subscribe_air_quality(aq_id, "current") 

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, topic, payload):
    print('Air Quality Update!')
    print('Air Quality record ID: {0}'.format(topic))
    print(payload)

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

client.connect()
client.loop_blocking()
