"""
'pi_camera.py'
=======================================
Example for sending pictures taken by
a Raspberry Pi camera to an
Adafruit IO feed.
"""
# import standard python modules
import time
import base64
import os

# import Adafruit IO REST client
from Adafruit_IO import Client, Feed, RequestError

# import raspberry pi camera module
import picamera

# camera capture interval, in seconds
CAMERA_INTERVAL = 3

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Adafruit IO Pi Camera Feed
# note: this feed requires its history to be
# turned off from the adafruit io feed page
picam_feed = aio.feeds('picam')

# set up picamera
camera = picamera.PiCamera()

# set the resolution of the camera's captures
# note: Adafruit IO feeds with history turned
# OFF only support images < 1kb
camera.resolution = (200, 200)

print('Adafruit IO: Raspberry Pi Camera Example')

while True:
  camera.capture('image.jpg')
  print('Camera: SNAP!')
  with open("image.jpg", "rb") as imageFile:
    image = base64.b64encode(imageFile.read())
    # encode the b64 bytearray as a string for adafruit-io
    image_string = image.decode("utf-8")
    try:
      aio.send(picam_feed.key, image_string)
      print('Picture sent to Adafruit IO')
    except:
      print('Sending to Adafruit IO Failed...')

  time.sleep(CAMERA_INTERVAL)
