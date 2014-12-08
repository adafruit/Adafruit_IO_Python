Adafruit IO Python Client Test README

To run these tests you must have the pytest module installed.  You can install
this (assuming you have pip installed) by executing:
  sudo pip install pytest

Some tests require a valid Adafruit IO account to run, and they key for this
account is provided in the ADAFRUIT_IO_KEY environment variable.  Make sure to
set this envirionment variable before running the tests, for example to run all
the tests with a key execute in this directory:
  ADAFRUIT_IO_KEY=my_io_key_value py.test
