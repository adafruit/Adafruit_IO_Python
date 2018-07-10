Data
----
Data represents the data contained in feeds. You can read, add, modify, and delete data. There are also a few convenient methods for sending data to feeds and selecting certain pieces of data.

Data Creation
~~~~~~~~~~~~~
Data can be created after you create a feed, by using the ``create_data(feed, data)`` method and passing it a new Data instance a value.

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client, Data
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Create a data item with value 10 in the 'Test' feed.
    data = Data(value=10)
    aio.create_data('Test', data)

Data Retrieval
~~~~~~~~~~~~~~~
You can get all of the data for a feed by using the ``data(feed)`` method. The result will be an array of all feed data, each returned as an instance of the Data class. Use the value property on each Data instance to get the data value, and remember values are always returned as strings (so you might need to convert to an int or number if you expect a numeric value).

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Get an array of all data from feed 'Test'
    data = aio.data('Test')

    # Print out all the results.
    for d in data:
        print('Data value: {0}'.format(d.value))

You can also get a specific value by ID by using the ``feeds(feed, data_id)`` method. This will return a single piece of feed data with the provided data ID if it exists in the feed. The returned object will be an instance of the Data class.


Data Deletion
~~~~~~~~~~~~~
Values can be deleted by using the ``delete(feed, data_id)`` method:

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Delete a data value from feed 'Test' with ID 1.
    data = aio.delete('Test', 1)

Data Helper methods
--------------------
There are a few helper methods that can make interacting with data a bit easier.

Send Data
~~~~~~~~~
You can use the ``send_data(feed_name, value)`` method to append a new value to a feed. This is the recommended way to send data to Adafruit IO from the Python REST client.

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Add the value 98.6 to the feed 'Temperature'.
    test = aio.feeds('test')
    aio.send_data(test.key, 98.6)

Send Batch Data
~~~~~~~~~~~~~~~
Data can be created after you create a feed, by using the ``send_batch_data(feed, data_list)`` method and passing it a new Data list.

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client, Data
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Create a data items in the 'Test' feed.
    data_list = [Data(value=10), Data(value=11)]
    aio.create_data('Test', data)


Receive Data
~~~~~~~~~~~~
You can get the last inserted value by using the ``receive(feed)`` method.

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Get the last value of the temperature feed.
    data = aio.receive('Test')

    # Print the value and a message if it's over 100.  Notice that the value is
    # converted from string to int because it always comes back as a string from IO.
    temp = int(data.value)
    print('Temperature: {0}'.format(temp))
    if temp > 100:
        print 'Hot enough for you?'


Next Value
~~~~~~~~~~
You can get the first inserted value that has not been processed (read) by using the ``receive_next(feed)`` method.

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Get next unread value from feed 'Test'.
    data = aio.receive_next('Test')

    # Print the value.
    print('Data value: {0}'.format(data.value))



Previous Value
~~~~~~~~~~~~~~
You can get the last record that has been processed (read) by using the ``receive_previous(feed)`` method.

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Get previous read value from feed 'Test'.
    data = aio.receive_previous('Test')

    # Print the value.
    print('Data value: {0}'.format(data.value))


Publishing and Subscribing
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can get a readable stream of live data from your feed using the included MQTT client class:

.. literalinclude:: ../examples/mqtt/mqtt_subscribe.py
