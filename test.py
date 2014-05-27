from Adafruit_IO import Client
io = Client('e2b0fac48ae32f324df4aa05247c16e991494b08')

r = io.send("Test Python", 12)
print r

r = io.receive("Test Python")
print r

r = io.receive_next("Test Python")
print r