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

import json, requests

# MQTT RC Error Types
MQTT_ERRORS   = [ 'Connection successful',
                  'Incorrect protocol version',
                  'Invalid Client ID',
                  'Server unavailable ',
                  'Bad username or password',
                  'Not authorized' ]

class AdafruitIOError(Exception):
    """Base class for all Adafruit IO request failures."""
    pass


class RequestError(Exception):
    """General error for a failed Adafruit IO request."""
    def __init__(self, response):
        error_message = self._parse_error(response)
        super(RequestError, self).__init__("Adafruit IO request failed: {0} {1} - {2}".format(
            response.status_code, response.reason, error_message))

    def _parse_error(self, response):
        content = response.json()
        try:
            return content['error']
        except ValueError:
            return ""


class ThrottlingError(AdafruitIOError):
    """Too many requests have been made to Adafruit IO in a short period of time.
    Reduce the rate of requests and try again later.
    """
    def __init__(self):
        super(ThrottlingError, self).__init__("Exceeded the limit of Adafruit IO "  \
            "requests in a short period of time. Please reduce the rate of requests " \
            "and try again later.")


class MQTTError(Exception):
    """Handles connection attempt failed errors.
    """
    def __init__(self, response):
        error = MQTT_ERRORS[response]
        super(MQTTError, self).__init__(error)
    pass