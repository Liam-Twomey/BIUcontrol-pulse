#!/usr/bin/env python3

import time
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

if __name__=='__main__':
    #create the i2c object for the trellis
    i2c_bus = busio.I2C(SCL, SDA)

    #create the trellis object and associate it to the the i2c object that was created
    trellis = NeoTrellis(i2c_bus)

    # some color definitions
    OFF = (0, 0, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 78, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (200, 200, 200)

    #set colors for each pixel button
    trellis.pixels[0] = GREEN
    trellis.pixels[1] = RED
    trellis.pixels[2] = PURPLE
    trellis.pixels[3] = ORANGE
    trellis.pixels[4] = BLUE
    trellis.pixels[5] = WHITE
    
    ok2plunge = False

    # this will be called when button events are received
    def pixel_button_action(event):
        # turn the LED off when a rising edge is detected
        if event.edge == NeoTrellis.EDGE_RISING:
            trellis.pixels[event.number] = OFF
        # turn the LED off when a rising edge is detected
        elif event.edge == NeoTrellis.EDGE_FALLING:
            if event.number == 0:
                print("Executing #0 power up")
                trellis.pixels[0] = GREEN
                ok2plunge = True
            elif event.number == 1:
                if ok2plunge:
                    print("Executing #1 spray and plunge")
                    trellis.pixels[1] = RED
            elif event.number == 2:
                if ok2plunge:
                    print("Executing #2 pulse and plunge")
                    trellis.pixels[2] = PURPLE
            elif event.number == 3:
                print("Executing #3 power down")
                trellis.pixels[3] = ORANGE
                ok2plunge = False
            elif event.number == 4:
                print("Executing #4 cleaning")
                trellis.pixels[4] = BLUE
            elif event.number == 5:
                print("Executing #5 dry fire")
                trellis.pixels[5] = WHITE
            else:
                print("Wrong button pressed")

    for i in range(6):
        #activate rising edge events on all keys
        trellis.activate_key(i, NeoTrellis.EDGE_RISING)
        #activate falling edge events on all keys
        trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
        #set all keys to trigger the blink callback
        trellis.callbacks[i] = pixel_button_action


    while True:
        #call the sync function call any triggered callbacks
        trellis.sync()
        #the trellis can only be read every 10 milliseconds or so
        time.sleep(.02)
        
