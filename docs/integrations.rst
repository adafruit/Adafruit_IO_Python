Service Integrations
--------------------
Adafruit IO provides integration services that can be used from both the REST client
and MQTT client.

Time Service
~~~~~~~~~~~~
REST
^^^^
Use ``receive_time(timezone=None)`` to retrieve time data as a Python ``struct_time``.

MQTT
^^^^
Use:

- ``subscribe_time(time)``
- ``unsubscribe_time(time)``

Where ``time`` is one of:

- ``millis``
- ``seconds``
- ``iso``

Example:

.. literalinclude:: ../examples/mqtt/mqtt_time.py

Random Data Service
~~~~~~~~~~~~~~~~~~~
REST
^^^^
Use ``receive_random(randomizer_id=None)`` to list randomizers or read one by ID.

MQTT
^^^^
Use:

- ``subscribe_randomizer(randomizer_id)``
- ``unsubscribe_randomizer(randomizer_id)``

Example:

.. literalinclude:: ../examples/api/random_data.py

Weather Service
~~~~~~~~~~~~~~~
REST
^^^^
Use:

- ``receive_weather(weather_id=None)``
- ``create_weather(weather_record)``
- ``delete_weather(weather_id)``

Examples:

.. literalinclude:: ../examples/api/weather.py

.. literalinclude:: ../examples/api/weather_create_delete.py

MQTT
^^^^
Use:

- ``subscribe_weather(weather_id, forecast_type)``
- ``unsubscribe_weather(weather_id, forecast_type)``

Where ``forecast_type`` is one of:

- ``current``
- ``forecast_minutes_5``
- ``forecast_minutes_30``
- ``forecast_hours_1``
- ``forecast_hours_2``
- ``forecast_hours_6``
- ``forecast_hours_24``
- ``forecast_days_1``
- ``forecast_days_2``
- ``forecast_days_5``

Example:

.. literalinclude:: ../examples/mqtt/mqtt_weather.py

Air Quality Service
~~~~~~~~~~~~~~~~~~~
Note: Air Quality service access requires an IO+ subscription.

REST
^^^^
Use:

- ``receive_air_quality(airq_location_id=None, forecast=None)``
- ``create_air_quality(air_quality_record)``
- ``delete_air_quality(air_quality_id)``

Where ``forecast`` is optional and can be one of:

- ``current``
- ``forecast_today``
- ``forecast_tomorrow``

Examples:

.. literalinclude:: ../examples/api/air_quality.py

.. literalinclude:: ../examples/api/air_quality_create_delete.py

MQTT
^^^^
Use:

- ``subscribe_air_quality(airq_location_id, forecast='current')``
- ``unsubscribe_air_quality(airq_location_id, forecast='current')``

Example:

.. literalinclude:: ../examples/mqtt/mqtt_air_quality.py
