"""
'dashboard.py'
=========================================
Creates a dashboard with 3 blocks and feed it data

Author(s): Doug Zobel
"""
import os
from time import sleep
from random import randrange
from Adafruit_IO import Client, Feed, Block, Dashboard, Layout

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME', '')

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure **not** to publish it when you publish this code!
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY', '')

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create a new feed named 'Dashboard Data' under the default group
feed = aio.create_feed(Feed(name="Dashboard Data"), "default")

# Fetch group info (group.id needed when adding feeds to blocks)
group = aio.groups("default")

# Create a new dashboard named 'Example Dashboard'
dashboard = aio.create_dashboard(Dashboard(name="Example Dashboard"))

# Create a line_chart
linechart = Block(name="Linechart Data",
                  visual_type = 'line_chart',
                  properties = {
                      "gridLines": True,
                      "historyHours": "2"},
                  # block_feeds expects a numeric feed_id, not the feed key
                  block_feeds = [{
                      "group_id": group.id,
                      "feed_id":  feed.id
                  }])
linechart = aio.create_block(dashboard.key, linechart)

# Create a gauge
gauge = Block(name="Gauge Data",
              visual_type = 'gauge',
              block_feeds = [{
                  "group_id": group.id,
                  "feed_id":  feed.id
              }])
gauge = aio.create_block(dashboard.key, gauge)

# Create a text stream
stream = Block(name="Stream Data",
               visual_type = 'stream',
               properties = {
                   "fontSize": "12",
                   "fontColor": "#63de00",
                   "showGroupName": "no"},
               block_feeds = [{
                   "group_id": group.id,
                   "feed_id":  feed.id
               }])
stream = aio.create_block(dashboard.key, stream)

# Update the large layout to:
# |----------------|
# |   Line Chart   |
# |----------------|
# | Gauge | Stream |
# |----------------|
layout = Layout(lg = [
                   {'x': 0, 'y': 0, 'w': 16, 'h': 4, 'i': str(linechart.id)},
                   {'x': 0, 'y': 4, 'w':  8, 'h': 4, 'i': str(gauge.id)},
                   {'x': 8, 'y': 4, 'w':  8, 'h': 4, 'i': str(stream.id)}])
aio.update_layout(dashboard.key, layout)

print("Dashboard created at: " +
      "https://io.adafruit.com/{0}/dashboards/{1}".format(ADAFRUIT_IO_USERNAME,
                                                          dashboard.key))
# Now send some data
value = 0
while True:
    value = (value + randrange(0, 10)) % 100
    print('sending data: ', value)
    aio.send_data(feed.key, value)
    sleep(3)
