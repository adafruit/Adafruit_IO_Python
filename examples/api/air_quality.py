"""
'air_quality.py'
================================================
Adafruit IO Air Quality Service
with Adafruit IO API (requires IO+ subscription)

Author(s): Tyeth Gundry for Adafruit Industries
"""
import json
import os
from Adafruit_IO import Client

ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME", "YOUR_IO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY", "YOUR_IO_KEY")

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# ID of the Air Quality record to retrieve
# You can find this ID by visiting your Air Quality integration page on Adafruit IO
AQ_ID = None  # Replace with your Air Quality record ID

CREATED_DEMO_RECORD = False  # will be used to track deletion
if AQ_ID is None:
    # fetch the list of air quality records to find the first ID
    print('No Air Quality record ID specified. Fetching list of records...')
    air_quality_records = aio.receive_air_quality()
    if air_quality_records:
        AQ_ID = air_quality_records[0]['id']
        print('Using Air Quality record ID: {0}'.format(AQ_ID))
    else:
        # attempt to create one if none exist (requires IO+ subscription)
        try:
            aq_record = {
                "location": "40.726190,-74.005360",
                "name": "New York City, NY",
                "provider": "open_meteo"  # 'airnow' [US] or 'open_meteo' [Global]
            }
            created_record = aio.create_air_quality(aq_record)
            AQ_ID = created_record['id']
            CREATED_DEMO_RECORD = True
            print('Created Air Quality record with ID: {0}'.format(AQ_ID))
        except Exception as e:
            print('Failed to create Air Quality record: {0}'.format(e))
            exit(1)

print('Retrieving Air Quality Data for Air Quality record ID: {0}'.format(AQ_ID))
air_quality = aio.receive_air_quality(AQ_ID)
print(json.dumps(air_quality, indent=2))

# Clean up the demo record if we created one
if CREATED_DEMO_RECORD:
    try:
        aio.delete_air_quality(AQ_ID)
        print('\nDeleted demo Air Quality record with ID: {0}'.format(AQ_ID))
    except Exception as e:
        print('Failed to delete demo Air Quality record: {0}'.format(e))