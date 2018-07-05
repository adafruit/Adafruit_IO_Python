Feeds
-----
Feeds are the core of the Adafruit IO system. The feed holds metadata about data that gets pushed, and you will have one feed for each type of data you send to the system. You can have separate feeds for each sensor in a project, or you can use one feed to contain JSON encoded data for all of your sensors.


Feed Creation
~~~~~~~~~~~~~
Create a feed by constructing a Feed instance with at least a name specified, and then pass it to the ``create_feed(feed)`` function:

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client, Feed
    aio = Client('YOUR ADAFRUIT IO KEY')

    # Create Feed object with name 'Foo'.
    feed = Feed(name='Foo')

    # Send the Feed to IO to create.
    # The returned object will contain all the details about the created feed.
    result = aio.create_feed(feed)

Note that you can use the send function to create a feed and send it a new value in a single call. It's recommended that you use send instead of manually constructing feed instances.

Feed  Retrieval
~~~~~~~~~~~~~~~
You can get a list of your feeds by using the ``feeds()`` method which will return a list of Feed instances:

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO KEY')

    # Get list of feeds.
    feeds = aio.feeds()

    # Print out the feed names:
    for f in feeds:
        print('Feed: {0}'.format(f.name))

Alternatively you can retrieve the metadata for a single feed by calling ``feeds(feed)`` and passing the ``name``, ``ID``, or ``key`` of a feed to retrieve:

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO KEY')

    # Get feed 'Foo'
    feed = aio.feeds('Foo')

    # Print out the feed metadata.
    print(feed)


Feed  Deletion
~~~~~~~~~~~~~~
You can delete a feed by ID, key, or name by calling ``delete_feed(feed)``. ALL data in the feed will be deleted after calling this API!

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Delete the feed with name 'Test'.
    aio.delete_feed('Test')

