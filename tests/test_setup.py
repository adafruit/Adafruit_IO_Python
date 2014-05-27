import pytest

from Adafruit_IO import Client

def teardown_module(module):
  pass

class TestSetup:    
  def test_set_key(self):
    key = "unique_key_id"
    io = Client(key)
    assert key == io.key
