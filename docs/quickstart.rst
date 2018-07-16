Quickstart
------------
Here's a short example of how to send a new value to a feed (creating the feed if it doesn't exist), and how to read the most recent value from the feed. This example uses the REST API.

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT USER', 'YOUR ADAFRUIT IO KEY')

    # Send the value 100 to a feed called 'Foo'.
    aio.send('Foo', 100)

    # Retrieve the most recent value from the feed 'Foo'.
    # Access the value by reading the `value` property on the returned Data object.
    # Note that all values retrieved from IO are strings so you might need to convert
    # them to an int or numeric type if you expect a number.
    data = aio.receive('Foo')
    print('Received value: {0}'.format(data.value))

If you want to be notified of feed changes immediately without polling, consider using the MQTT client. See the ``examples/mqtt_client.py`` for an example of using the MQTT client.

Basic Client Usage
-------------------

You must have an Adafruit IO key to use this library and the Adafruit IO service. Your API key will be provided to the python library so it can authenticate your requests against the Adafruit IO service.

At a high level the Adafruit IO python client provides two interfaces to the service:

- A thin wrapper around the REST-based API. This is good for simple request and response applications like logging data.

- A MQTT client (based on paho-mqtt) which can publish and subscribe to feeds so it is immediately alerted of changes. This is good for applications which need to know when something has changed as quickly as possible.

To use either interface you'll first need to import the python client by adding an import such as the following at the top of your program:

.. code-block:: python

    from Adafruit_IO import *

Then a REST API client can be created with code like:

.. code-block:: python

    aio = Client('user', 'xxxxxxxxxxxx')

Where ``'xxxxxxxxxxxx'`` is your Adafruit IO API key.
Where ``'user'`` is your Adafruit username.


Alternatively an MQTT client can be created with code like:

.. code-block:: python

    mqtt = MQTTClient('user', 'xxxxxxxxxxxx')

Again where ``'xxxxxxxxxxxx'`` is your Adafruit IO API key.
Again where ``'user'`` is your Adafruit username.

Your program can use either or both the REST API client and MQTT client, depending on your needs.

Error Handling
---------------
The python client library will raise an exception if it runs into an error it cannot handle. 
You should be prepared to catch explicit exceptions you know how to handle, or bubble them up to the user as an error. 
Adafruit IO exceptions generally are children of the base exception type AdafruitIOError. There are also three sub-exceptions to handle, depending on which if you're using the REST API 
or MQTT Client: MQTTError (for the MQTT Client), RequestError (REST Client), and ThrottlingError (REST Client).

