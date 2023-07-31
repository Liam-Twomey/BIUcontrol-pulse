#!/usr/bin/env python3

from guizero import App, TextBox, Text, PushButton, CheckBox
import RPi.GPIO as GPIO
#import gpio as GPIO
import BIUpinlist as pin

from BIU_gui_callback_functions import *

# def pedal():
#     GPIO.setup(pin.pedalsensor,GPIO.IN, pull_up_down = GPIO.PUD_UP)
#     if button_start.enabled and GPIO.input(pin.pedalsensor)==0:
#         print("Pedal triggered")
#         startprocess()

def text_box(app, disp:str, position:list, default):
    '''
    Takes in app as zerogui application object, and then return the following to the caller of this function:
        label: a zerogui Text object
        box : a zerogui TextBox object
    '''
    if len(position) == 2:
        posbox = [position[0]+1, position[1]]
    else:
        print('Incorrect number of arguments to text_box.')
        return
    label =    Text(app, grid = position, text = disp,  align = 'left')
    box   = TextBox(app, grid=posbox,     text=str(default), align='left')
    box.text_size = 12
    return label, box

if __name__=='__main__':
    app = App(title="Back-it-up", layout="grid", width = 600, height = 330)
    
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

    ## Buttons, commands are defined in BIU_gui_callback_functions.py
    button_title = Text(master=app, text="Triggers", grid=[0,9,2,1], color='white', bg='dim grey')
    donotplunge = CheckBox(master=app, text="Dry fire (do not plunge)?",   grid=[0,10,2,1], align='left')

    button_pulse= PushButton(master=app, text="Pulse & Plunge", grid=[2,11], align='left', command=pulsestartprocess, args = [rdelay, pdelay, plen, donotplunge.value==1])
    button_pulse.disable()
    button_pulse.bg = 'violet'

    button_start= PushButton(master=app, text="Spray & Plunge", grid=[1,11], align='left', command=startprocess, args=[stime, rdelay, pdelay, donotplunge.value==1])
    button_start.bg = (255, 50, 50)
    button_start.disable()

    button_up   = PushButton(master=app, text="  Ready  ", grid=[0,11], align='left', command=powerup, args = [[button_start, button_pulse]])
    button_up.bg="lime green"

    button_down = PushButton(master=app, text="  Abort  ", grid=[3,11], align='left', command=powerdown, args = [[button_start, button_pulse]])
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
    app.display()

    #shutdown
    print('BIU program shutting down...')
    powerdown([button_start, button_pulse])
    # GPIO.cleanup()
    

