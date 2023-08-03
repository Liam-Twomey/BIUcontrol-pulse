#!/usr/bin/env python3

import time
import board
from adafruit_neotrellis.neotrellis import NeoTrellis

# create the i2c object for the trellis
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# create a callback function
def key_event(event):
    if event.number in range(6):
        if event.edge == NeoTrellis.EDGE_RISING:
            trellis.pixels[event.number] = key_colors[event.number]
        elif event.edge == NeoTrellis.EDGE_FALLING:
            trellis.pixels[event.number] = (0, 0, 0)

# create the trellis
trellis = NeoTrellis(i2c_bus)

# Set the brightness value (0 to 1.0)
trellis.brightness = 0.5

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255

# activate rising and falling edge events on all keys
for i in range(6):
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    trellis.callbacks[i] = key_event

while True:
    # call the sync function to update the trellis state
    trellis.sync()
