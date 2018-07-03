Groups
-------
Groups allow you to update and retrieve multiple feeds with one request. You can add feeds to multiple groups.


Group Creation
~~~~~~~~~~~~~~
The creation of groups is now supported in API-V2, rejoyce! The process of creating a group is similar to creating a feed.
Create a group by constructing a Group instance with at least a name specified, and then pass it to the ``create_group(group)`` function:

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client, Group
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Create a group instance
    group = Group(name="weatherstation")

    # Send the group for IO to create:
    # The returned object will contain all the details about the created group.
    group = aio.create_group(group


Group Retrieval
~~~~~~~~~~~~~~~
You can get a list of your groups by using the ``groups()`` method. 
This will return a list of Group instances. Each Group instance has metadata about the group, including a ``feeds`` property which is a tuple of all feeds in the group.


.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Get list of groups.
    groups = aio.groups()

    # Print the group names and number of feeds in the group.
    for g in groups:
        print('Group {0} has {1} feed(s).'.format(g.name, len(g.feeds)))


You can also get a specific group by ID, key, or name by using the ``groups(group)`` method:

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Get group called 'GroupTest'.
    group = aio.groups('GroupTest')

    # Print the group name and number of feeds in the group.
    print('Group {0} has {1} feed(s).'.format(group.name, len(group.feeds)))

Group Updating
~~~~~~~~~~~~~~
TODO: Test and example this 

Group Deletion
~~~~~~~~~~~~~~
You can delete a group by ID, key, or name by using the ``delete_group(group)`` method:

.. code-block:: python

    # Import library and create instance of REST client.
    from Adafruit_IO import Client
    aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')

    # Delete group called 'GroupTest'.
    aio.delete_group('GroupTest')

