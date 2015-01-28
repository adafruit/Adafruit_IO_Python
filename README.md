# adafruit-io

A [Python][1] client for use with with [io.adafruit.com][2].

## Installation

### Easy Installation

If you have [pip installed](https://pip.pypa.io/en/latest/installing.html) 
(typically with ````apt-get install python-pip```` on a Debian/Ubuntu-based 
system) then run:

    sudo pip install adafruit-io

### Manual Installation

Clone or download the contents of this repository.  Then navigate to the folder
in a terminal and run the following command:

    sudo python setup.py install

(on Windows omit the sudo)

## Usage

You must have an [Adafruit IO key][4] to use this library and the Adafruit IO service.
Your API key will be provided to the python library so it can authenticate your 
requests against the Adafruit IO service.

At a high level the Adafruit IO python client provides two interfaces to the
service:

* A thin wrapper around the REST-based API.  This is good for simple request and
  response applications.

* An MQTT client (based on [paho-mqtt](https://pypi.python.org/pypi/paho-mqtt)) 
  which can publish and subscribe to feeds so it is immediately alerted of changes.
  This is good for applications which need to know when something has changed as
  quickly as possible, but requires keeping a connection to the service open at
  all times.

To use either interface you'll first need to import the python client by adding
an import such as the following at the top of your program:

```python
import Adafruit_IO
```

Then a REST API client can be created with code like:

```python
aio = Adafruit_IO.Client('xxxxxxxxxxxx')
```

Where 'xxxxxxxxxxxx' is your Adafruit IO API key.

Alternatively an MQTT client can be created with code like:

```python
mqtt = Adafruit_IO.MQTTClient('xxxxxxxxxxxx')
```

Again where 'xxxxxxxxxxxx' is your Adafruit IO API key.

Your program can use either or both the REST API client and MQTT client, 
depending on your needs.

### Error Handling

The python client library will raise an exception if it runs into an error it
cannot handle.  You should be prepared to catch explicit exceptions you know how
to handle, or bubble them up to the user as an error.  Adafruit IO exceptions
generally are children of the base exception type `AdafruitIOError`.

### Quickstart

Here's a short example of how to send a new value to a feed (creating the feed 
if it doesn't exist), and how to read the most recent value from the feed.  This
example uses the REST API.

```python
# Import library and create instance of REST client.
from Adafruit_IO import Client
aio = Client('YOUR ADAFRUIT IO KEY')

# Send a value to a feed called 'Feed Name'.
# Data can be of any type, string, number, hash, json.
aio.send('Feed Name', data)

# Retrieve the most recent value from the feed 'Feed Name'.
# Notice the returned object has a property called value.
data = aio.receive("Feed Name")
print('Received value: {0}'.format(data.value))
```

If you want to be notified of feed changes immediately without polling, consider
using the MQTT client.  See the [examples\mqtt_client.py](https://github.com/adafruit/io-client-python/blob/master/examples/mqtt_client.py) for an example of using the MQTT client.

## Table of Contents

* [Feeds](#feeds)
  * [Creation, Retrieval, Updating](#feed-creation-retrieval-updating)
  * [Delete](#feed-deletion)
* [Data](#data)
  * [Create](#data-creation)
  * [Read](#data-retrieval)
  * [Updating, Deletion](#data-updating-deletion)
  * [Helper Methods](#helper-methods)
    * [Send](#send)
    * [Receive](#receive)
    * [Next](#next)
    * [Previous](#previous)
  * [Publishing and Subscribing](#publishing-and-subscribing)
* [Groups](#groups)

### Feeds

[Feeds][3] are the core of the Adafruit IO system. The feed holds metadata about data
that gets pushed, and you will have one feed for each type of data you send to 
the system. You can have separate feeds for each sensor in a project, or you can
use one feed to contain JSON encoded data for all of your sensors.

#### Feed Creation, Retrieval, Updating

TODO: The python client does not currently support creating, retrieving, or 
updating a feed's metadata.  See the send helper function below for creating a
feed and sending it new data.

#### Feed Deletion

You can delete a feed by ID, key, or name by calling `aio.delete_feed(feed)`.
ALL data in the feed will be deleted after calling this API!

```python
# Delete the feed with name 'Test'.
aio.delete_feed('Test')
```

### Data

Data represents the data contained in feeds. You can read, add, modify, and 
delete data. There are also a few convienient methods for sending data to feeds
and selecting certain pieces of data.

#### Data Creation

Data can be created [after you create a feed](#data-creation), by using the
`aio.create_data(feed, data)` method and passing it a new Data instance with
a value set.  See the [send function](#send) for a simpler and recommended way
of adding a new value to a feed.

```python
# Create a data item with value 10 in the 'Test' feed.
data = Adafruit_IO.Data(value=10)
aio.create_stream('Test', data)
```

#### Data Retrieval

You can get all of the data for a feed by using the `aio.data(feed)` method. The
result will be an array of all feed data, each returned as an instance of the
Data class.  Use the value property on each Data instance to get the data value.

```python
# Get an array of all data from feed 'Test'
data = aio.streams('Test')
# Print out all the results.
for d in data:
    print('Data value: {0}'.format(d.value))
```

You can also get a specific value by ID by using the `aio.feeds(feed, data_id)`
method.  This will return a single piece of feed data with the provided data ID
if it exists in the feed.  The returned object will be an instance of the Data
class.

```python
# Get a specific value by id.
# This example assumes 1 is a valid data ID in the 'Test' feed
data = aio.feeds('Test', 1)
# Print the value.
print('Data value: {0}'.format(data.value))
```

#### Data Updating, Deletion

TODO: The python client does not currently support updating or deleting feed 
data.

#### Helper Methods

There are a few helper methods that can make interacting with data a bit easier.

##### Send

You can use the `aio.send(feed_name, value)` method to append a new value to a
feed in one call.  If the specified feed does not exist it will automatically be
created.  This is the recommended way to send data to Adafruit IO from the Python
client.

```python
# Add the value 98.6 to the feed 'Test Send Data'.
aio.send('Test Send Data', 98.6)
```

##### Receive

You can get the last inserted value by using the `aio.receive(feed)` method.

```python
data = aio.receive('Test')
# Print the value.
print('Data value: {0}'.format(data))
```

##### Next

You can get the first inserted value that has not been processed by using the
`aio.receive_next(feed)` method.

```python
data = aio.receive_next('Test')
# Print the value.
print('Data value: {0}'.format(data))
```

##### Previous

You can get the the last record that has been processed by using the 
`aio.receive_previous(feed)` method.

```python
data = aio.receive_previous('Test')
# Print the value.
print('Data value: {0}'.format(data))
```

#### Publishing and Subscribing

You can get a readable stream of live data from your feed using the included
MQTT client class.

TBD: Document using the MQTT client.

### Groups

Groups allow you to update and retrieve multiple feeds with one request. You can 
add feeds to multiple groups.

TBD

## Contributing

1. Fork it ( http://github.com/adafruit/io-client-python/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## License
Copyright (c) 2014 Adafruit Industries. Licensed under the MIT license.

[1]: https://www.python.org/
[2]: https://io.adafruit.com
[3]: https://learn.adafruit.com/adafruit-io/feeds
[4]: https://learn.adafruit.com/adafruit-io/api-key
[5]: https://learn.adafruit.com/adafruit-io/groups
