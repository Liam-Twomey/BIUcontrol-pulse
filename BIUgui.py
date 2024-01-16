#!/usr/bin/env python3

from guizero import App, TextBox, Text, PushButton, CheckBox
#try: # for RPi
import RPi.GPIO as GPIO
#except: #if PC:
#    import gpio as GPIO
import BIUpinlist as pin
from BIU_gui_helper_functions import *

# OPTIONS
use_neotrellis = True
# Neotrellis options
if use_neotrellis:
    from board import SCL, SDA
    import busio
    from adafruit_neotrellis.neotrellis import NeoTrellis

stateTracker = UserProgressTracker()

if __name__=='__main__':
    app = App(title="Back-it-up", layout="grid", width = 600, height = 340)
    
    # GUI for Standard Spray parameters entries
    stdlabel            = Text(app, text="Standard Spray", color='white', grid=[0,0,2,1], bg = 'dim gray')
    stimelabel, stime   = text_box(app, 'Spray time (ms):',       position = [0,1], default = 30)
    rdelaylabel, rdelay = text_box(app, 'Retraction delay (ms):', position = [0,2], default = 50)
    pdelaylabel, pdelay = text_box(app, 'Plunge delay (ms):',     position = [0,3], default = 50)

    # GUI for Pulse Spray parameters entries
    pulselabel  = Text(app, text="(Anti) Pulse Spray", grid=[0,4,2,1], color='white', bg='dim gray')
    plen_label, plen   = text_box(app, 'Pulse length (ms):',   position = [0,5], default = 16)
    pnum_label, pnum   = text_box(app, 'Pulse count:',   position = [0,6], default = 5)
    pint_label, pint   = text_box(app, 'Pulse interval (ms):',   position = [0,7], default = 20)
    pulsenote            = Text(app, text="(Uses retraction & plunge settings from std.)", grid=[0,8,2,1])

    ## Buttons, commands are defined in BIU_gui_helper_functions.py
    button_title = Text(master=app, text="Triggers", grid=[0,9,4,1], color='white', bg='dim grey')
    donotplunge = CheckBox(master=app, text="Dry fire (do not plunge)?",   grid=[0,10,2,1], align='left')

    button_pulse= PushButton(master=app, text="Pulse & Plunge", grid=[2,11], align='left', command=pulsestartprocess, args = [stateTracker,rdelay, pdelay, pnum, plen, pint, donotplunge.value==1])
    button_pulse.disable()
    button_pulse.bg = 'violet'

    button_start= PushButton(master=app, text="Spray & Plunge", grid=[1,11], align='left', command=startprocess, args=[stateTracker,stime, rdelay, pdelay, donotplunge.value==1])
    button_start.bg = (255, 50, 50)
    button_start.disable()

    button_up   = PushButton(master=app, text="  Ready  ", grid=[0,11], align='left', command=powerup, args = [stateTracker,[button_start, button_pulse]])
    button_up.bg="lime green"

    button_down = PushButton(master=app, text="  Abort  ", grid=[3,11], align='left', command=powerdown, args = [stateTracker,[button_start, button_pulse]])
    button_down.bg = "orange"
        
    # GUI for Cleaning operation
    cleanlabel    = Text(app, text="Cleaning settings:", grid=[2,0,2,1], color='white', bg='dim gray')
    cleancycleslabel, cleancycles = text_box(app, 'Cleaning cycles:',     position = [2,1], default = 5)
    cleantimelabel, cleantime = text_box(app, 'Clean pulse length (ms):', position = [2,2], default = 200)
    ## Buttons
    button_clean = PushButton(master = app, text=" Clean ", grid=[2,3,2,1], command=cleanprocess, args = [cleantime, cleancycles])
    button_clean.bg = "lightblue"

    for element in [button_up, button_start, donotplunge, button_down, button_clean, button_pulse]:
        element.text_size = 12

    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # app.repeat(100,pedal)

    if use_neotrellis:
        # create the i2c object for the trellis
        i2c_bus = busio.I2C(SCL, SDA)

        # create the trellis object and associate it to the the i2c object that was created
        trellis = NeoTrellis(i2c_bus)

        # some color definitions
        OFF = (0, 0, 0)
        RED = (255, 0, 0)
        ORANGE = (255, 78, 0)
        GREEN = (0, 255, 0)
        BLUE = (10, 10, 255)
        PURPLE = (90, 0, 255)
        WHITE = (200, 200, 200)
        YELLOW = (200, 200, 0)

        # set brightness of the trellis
        trellis.brightness = 0.5

        # set colors for each pixel button
        trellis.pixels[0] = GREEN
        trellis.pixels[3] = ORANGE
        trellis.pixels[4] = BLUE
        trellis.pixels[7] = WHITE

        ok2plunge = False


        # this will be called when button events are received
        def pixel_button_action(event):
            global ok2plunge, button_start, button_pulse, stime, rdelay, pdelay, donotplunge, plen, cleantime, cleancycles, pint, pnum
            # turn the LED off when a rising edge is detected
            if event.edge == NeoTrellis.EDGE_RISING:
                trellis.pixels[event.number] = OFF
            # turn the LED off when a rising edge is detected
            elif event.edge == NeoTrellis.EDGE_FALLING:
                if event.number == 0:
                    print("Trellis: Executing #0 power up")
                    powerup([button_start, button_pulse])
                    trellis.pixels[0] = GREEN
                    ok2plunge = True
                    trellis.pixels[1] = RED
                    trellis.pixels[2] = PURPLE
                elif event.number == 1:
                    if ok2plunge:
                        print("Trellis: Executing #1 spray and plunge")
                        startprocess(stime, rdelay, pdelay, donotplunge.value==1)
                        trellis.pixels[1] = RED
                elif event.number == 2:
                    if ok2plunge:
                        print("Trellis: Executing #2 pulse and plunge")
                        pulsestartprocess(rdelay, pdelay, pnum, plen, pint, donotplunge.value==1)
                        trellis.pixels[2] = PURPLE
                elif event.number == 3:
                    print("Trellis: Executing #3 power down")
                    powerdown([button_start, button_pulse])
                    trellis.pixels[3] = ORANGE
                    ok2plunge = False
                    trellis.pixels[1] = OFF
                    trellis.pixels[2] = OFF
                elif event.number == 4:
                    print("Trellis: Executing #4 cleaning")
                    cleanprocess(cleantime, cleancycles)
                    trellis.pixels[4] = BLUE
                elif event.number == 7:
                    if donotplunge.value == 0:
                        print("Trellis: Executing #7 dry fire")
                        donotplunge.value = 1
                        trellis.pixels[7] = YELLOW
                    else:
                        print("Trellis: Toggle off #7 dry fire")
                        donotplunge.value = 0
                        trellis.pixels[7] = WHITE
                else:
                    print("Trellis: Wrong button pressed")


        for i in [0, 1, 2, 3, 4, 7]:
            # activate rising edge events on all keys
            trellis.activate_key(i, NeoTrellis.EDGE_RISING)
            # activate falling edge events on all keys
            trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
            # set all keys to trigger the blink callback
            trellis.callbacks[i] = pixel_button_action
            
        def gui_repeating_tasks():
            global trellis, button_start
            trellis.sync()
            if donotplunge.value==1:
                trellis.pixels[7] = YELLOW
            else:
                trellis.pixels[7] = WHITE
            if button_start.enabled:
                ok2plunge = True
                trellis.pixels[1] = RED
                trellis.pixels[2] = PURPLE
            else:
                ok2plunge = False
                trellis.pixels[1] = OFF
                trellis.pixels[2] = OFF    
            
        app.repeat(90, gui_repeating_tasks)

    app.display()

    #shutdown
    print('BIU program shutting down...')
    if use_neotrellis:
        for i in [0, 1, 2, 3, 4, 7]: 
            trellis.pixels[i] = OFF

    powerdown(stateTracker,[button_start, button_pulse])
    GPIO.cleanup()
    

