# adafruit-io

A [Python][1] client for use with with [io.adafruit.com][2].

## Installation

    pip install adafruit-io

## Usage

  Easiest
  
    from Adafruit_IO import Client
    aio = Client('unique_key_id')
    #data can be of any type, string, number, hash, json
    aio.send("Feed Name", data)

    #You can also receive data easily:
    value = aio.receive("Feed Name")

    #It will ge the next input available, and mark it as read.


  Advanced

    from Adafruit_IO import Client
    aio = Client('unique_key_id')

    #get all of your feeds for the key
    aio.feeds

    #get a specific feed using ID or Name
    aio.feeds(3)
    aio.feeds("feed name")

    #create a feed
    aio.create_feed({:name => "New Feed Name", ...})

  MQTT/Publish-Subscribe
  
  Avoid the overhead of polling so you can immediately be notified of changes in a feed by using the 
  MQTT-based client.  Make sure the paho-mqtt package is installed (````sudo pip install paho-mqtt````), 
  then check out the [examples\mqtt_client.py](https://github.com/adafruit/io-client-python/blob/master/examples/mqtt_client.py) example for more details.

## Contributing

1. Fork it ( http://github.com/adafruit/io-client-python/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

[1]: https://www.python.org/
[2]: https://io.adafruit.com
