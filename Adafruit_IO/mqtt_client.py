# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging

import paho.mqtt.client as mqtt
import sys
from .errors import MQTTError, RequestError

# How long to wait before sending a keep alive (paho-mqtt configuration).
KEEP_ALIVE_SEC = 60  # One minute

logger = logging.getLogger(__name__)


class MQTTClient(object):
    """Interface for publishing and subscribing to feed changes on Adafruit IO
    using the MQTT protocol.
    """

    def __init__(self, username, key, service_host='io.adafruit.com', secure=True):
        """Create instance of MQTT client.

            :param username: Adafruit.IO Username for your account.
            :param key: Adafruit IO access key (AIO Key) for your account.
            :param secure: (optional, boolean) Switches secure/insecure connections
        """
        self._username = username
        self._service_host = service_host
        if secure:
            self._service_port = 8883
        elif not secure:
            self._service_port = 1883
        # Initialize event callbacks to be None so they don't fire.
        self.on_connect    = None
        self.on_disconnect = None
        self.on_message    = None
        # Initialize MQTT client.
        self._client = mqtt.Client()
        if secure:
            self._client.tls_set_context()
            self._secure = True
        elif not secure:
            print('**THIS CONNECTION IS INSECURE** SSL/TLS not supported for this platform')
            self._secure = False
        self._client.username_pw_set(username, key)
        self._client.on_connect    = self._mqtt_connect
        self._client.on_disconnect = self._mqtt_disconnect
        self._client.on_message    = self._mqtt_message
        self._connected = False

    def _mqtt_connect(self, client, userdata, flags, rc):
        logger.debug('Client on_connect called.')
        # Check if the result code is success (0) or some error (non-zero) and
        # raise an exception if failed.
        if rc == 0:
            #raise RequestError(rc)
            self._connected = True
            print('Connected to Adafruit IO!')
        else:
            # handle RC errors within `errors.py`'s MQTTError class
            raise MQTTError(rc)
        # Call the on_connect callback if available.
        if self.on_connect is not None:
            self.on_connect(self)

    def _mqtt_disconnect(self, client, userdata, rc):
        logger.debug('Client on_disconnect called.')
        self._connected = False
        # If this was an unexpected disconnect (non-zero result code) then just
        # log the RC as an error.  Continue on to call any disconnect handler
        # so clients can potentially recover gracefully.
        if rc != 0:
            raise MQTTError(rc)
        print('Disconnected from Adafruit IO!')
        # Call the on_disconnect callback if available.
        if self.on_disconnect is not None:
            self.on_disconnect(self)

    def _mqtt_message(self, client, userdata, msg):
        logger.debug('Client on_message called.')
        # Parse out the feed id and call on_message callback.
        # Assumes topic looks like "username/feeds/id"
        parsed_topic = msg.topic.split('/')
        if self.on_message is not None and self._username == parsed_topic[0]:
            feed = parsed_topic[2]
            payload = '' if msg.payload is None else msg.payload.decode('utf-8')
        elif self.on_message is not None and parsed_topic[0] == 'time':
            feed = parsed_topic[0]
            payload = msg.payload.decode('utf-8')
        self.on_message(self, feed, payload)

    def connect(self, **kwargs):
        """Connect to the Adafruit.IO service.  Must be called before any loop
        or publish operations are called.  Will raise an exception if a
        connection cannot be made.  Optional keyword arguments will be passed
        to paho-mqtt client connect function.
        """
        # Skip calling connect if already connected.
        if self._connected:
            return
        # If given, use user-provided keepalive, otherwise default to KEEP_ALIVE_SEC
        keepalive = kwargs.pop('keepalive', KEEP_ALIVE_SEC)
        # Connect to the Adafruit IO MQTT service.
        self._client.connect(self._service_host, port=self._service_port,
            keepalive=keepalive, **kwargs)

    def is_connected(self):
        """Returns True if connected to Adafruit.IO and False if not connected.
        """
        return self._connected

    def disconnect(self):
        """Disconnect MQTT client if connected."""
        if self._connected:
            self._client.disconnect()

    def loop_background(self):
        """Starts a background thread to listen for messages from Adafruit.IO
        and call the appropriate callbacks when feed events occur.  Will return
        immediately and will not block execution.  Should only be called once.
        """
        self._client.loop_start()

    def loop_blocking(self):
        """Listen for messages from Adafruit.IO and call the appropriate
        callbacks when feed events occur.  This call will block execution of
        your program and will not return until disconnect is explicitly called.

        This is useful if your program doesn't need to do anything else except
        listen and respond to Adafruit.IO feed events.  If you need to do other
        processing, consider using the loop_background function to run a loop
        in the background.
        """
        self._client.loop_forever()

    def loop(self, timeout_sec=1.0):
        """Manually process messages from Adafruit.IO.  This is meant to be used
        inside your own main loop, where you periodically call this function to
        make sure messages are being processed to and from Adafruit_IO.

        The optional timeout_sec parameter specifies at most how long to block
        execution waiting for messages when this function is called.  The default
        is one second.
        """
        self._client.loop(timeout=timeout_sec)

    def subscribe(self, feed_id):
        """Subscribe to changes on the specified feed.  When the feed is updated
        the on_message function will be called with the feed_id and new value.
        """
        self._client.subscribe('{0}/feeds/{1}'.format(self._username, feed_id))

    def subscribe_time(self, time):
        """Subscribe to changes on the Adafruit IO time feeds. When the feed is
        updated, the on_message function will be called and publish a new value:
        time =
            millis: milliseconds
            seconds: seconds
            iso: ISO-8601 (https://en.wikipedia.org/wiki/ISO_8601)
        """
        if time == 'millis' or time == 'seconds':
            self._client.subscribe('time/{0}'.format(time))
        elif time == 'iso':
            self._client.subscribe('time/ISO-8601')
        else:
            print('ERROR: Invalid time type specified')
            return

    def publish(self, feed_id, value):
        """Publish a value to a specified feed.

        Required parameters:
        - feed_id: The id of the feed to update.
        - value: The new value to publish to the feed.
        """
        self._client.publish('{0}/feeds/{1}'.format(self._username, feed_id),
            payload=value)
