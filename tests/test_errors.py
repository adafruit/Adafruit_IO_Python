import os
import time

import pytest

import Adafruit_IO


def _get_client():
  """Return an Adafruit IO client instance configured with the key specified in
  the ADAFRUIT_IO_KEY environment variable.
  """
  key = os.environ.get('ADAFRUIT_IO_KEY', None)
  if key is None:
    raise RuntimeError("ADAFRUIT_IO_KEY environment variable must be set with " \
      "valid Adafruit IO key to run this test!")
  return Adafruit_IO.Client(key)


class TestErrors:    
  def test_request_error_from_bad_key(self):
    io = Adafruit_IO.Client("this is a bad key from a test")
    with pytest.raises(Adafruit_IO.RequestError):
      io.send("TestStream", 42)

  def test_throttling_error_after_6_requests_in_short_period(self):
    io = _get_client()
    with pytest.raises(Adafruit_IO.ThrottlingError):
      for i in range(6):
        io.send("TestStream", 42)
        time.sleep(0.1)  # Small delay to keep from hammering network.
