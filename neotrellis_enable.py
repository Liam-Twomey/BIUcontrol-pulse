#!/usr/bin/env python3

import time
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# create the trellis
trellis = NeoTrellis(i2c_bus)

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)


def blink(event, index):
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        if index == 0:
            trellis.pixels[event.number] = GREEN
        elif index == 1:
            trellis.pixels[event.number] = RED
        elif index == 2:
            trellis.pixels[event.number] = PURPLE
        elif index == 3:
            trellis.pixels[event.number] = ORANGE
        elif index == 4:
            trellis.pixels[event.number] = BLUE
        else:
            trellis.pixels[event.number] = WHITE
    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = OFF


for i in [0, 1, 2, 3, 4, 5]:
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink(i)

while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 10 millisecons or so
    time.sleep(.02)
