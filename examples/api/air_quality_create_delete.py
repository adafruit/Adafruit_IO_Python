"""
'air_quality_create_delete.py'
================================================
Create and Delete Air Quality Records
with Adafruit IO API

Author(s): Brent Rubell for Adafruit Industries
"""
import os
from Adafruit_IO import Client, RequestError

ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME", "YOUR_IO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY", "YOUR_IO_KEY")

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create a new air quality record
print('Creating new air quality record...')
aq_record = {
    'location': "40.726190,-74.005360",
    'name': 'New York City, NY',
    'provider': 'open_meteo'  # 'airnow' [US only] or 'open_meteo' [Global]
}
try:
    created_record = aio.create_air_quality(aq_record)
    print('Air Quality record created with ID: {0}'.format(created_record['id']))
    print(created_record)
    
    # Delete the air quality record
    print('\nDeleting air quality record...')
    aio.delete_air_quality(created_record['id'])
    print('Air Quality record deleted.')
except RequestError as e:
    print('Error: {0}'.format(e))
