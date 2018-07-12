2.0.0
- Drop support for API V1. Defaults to API V2
- MQTT/SSL support is now default.
- Add support for Python3
- New send_batch_data method
- Add error messages from response body in RequestError
- Add error messages from MQTT in MQTTError
- New location (lat/lon/ele) support
- New time topics support
- New examples added
- Unit tests updated to support API V2

0.9.0
----
Author: Tony DiCola
- Added REST API support for all feed, data, group create/get/update/delete APIs.
- Added explicit data model classes.
- Added many integration tests to verify client & service.
- Added docstrings to all public functions and classes.
- Ported to work with Python 2 and 3.

0.0.1
----
Initial Changelog
