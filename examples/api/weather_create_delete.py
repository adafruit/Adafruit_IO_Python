"""
'weather_create_delete.py'
================================================
Create and Delete Weather Records
with Adafruit IO API

Author(s): Brent Rubell for Adafruit Industries
"""
import os
from Adafruit_IO import Client, RequestError

ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME", "YOUR_IO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY", "YOUR_IO_KEY")

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create a new weather record
print('Creating new weather record...')
weather_record = {
    'location': "40.726190,-74.005360",
    'name': 'New York City, NY'
}
try:
    created_record = aio.create_weather(weather_record)
    print('Weather record created with ID: {0}'.format(created_record['id']))
    # Print the created record details (JSON, but compact form)
    print("Record details:")
    print(created_record, end='\n\n')
    
    # Delete the weather record
    print('Deleting weather record...')
    aio.delete_weather(created_record['id'])
    print('Weather record deleted.')
except RequestError as e:
    print('Error: {0}'.format(e))
