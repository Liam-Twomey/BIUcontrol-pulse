#!/usr/bin/env python3

from guizero import App, TextBox, Text, PushButton, CheckBox
from subprocess import call, Popen
#import RPi.GPIO as GPIO
import gpio as GPIO
import BIUpinlist as pin

def startprocess():
    print("Starting spray process.")
    spraytime        = str(float(stime.value)/1000)
    retractiondelay  = str(float(rdelay.value)/1000)
    plungedelay      = str(float(pdelay.value)/1000)
    arguments = ["python3","BIUapplyandplunge.py","--pulse",False,"--stime",spraytime,"--rdelay",retractiondelay,"--pdelay",plungedelay]
    if donotplunge.value==1:
        arguments.append("--donotplunge")
    call(arguments)
    button_start.disable()
    
def powerup():
    print("Power up")
    arguments = ["python3","BIUpowerupdown.py","--updown","up"]
    call(arguments)
    try:
        button_start.enable()
    except:
        return
def powerdown():
    print("Power down")
    arguments = ["python3","BIUpowerupdown.py","--updown","down"]
    call(arguments)
    try:
        button_start.disable()
    except:
        return
    
def pulsestartprocess():
    print("Starting pulse spray.")
    spraytime        = str(float(stime.value)/1000)
    retractiondelay  = str(float(rdelay.value)/1000)
    plungedelay      = str(float(pdelay.value)/1000)
    pulsecount       = str(float(pnum.value)/1000)
    pulselength       = str(float(plen.value)/1000)
    arguments = ["python3","BIUapplyandplunge.py","--pulse",True,"--pulseno",pulsecount,"--pulselen",pulselength,"--rdelay",retractiondelay,"--pdelay",plungedelay]
    if donotplunge.value==1:
        arguments.append("--donotplunge")
    call(arguments)
    button_start.disable()

def cleanprocess():
    print("Starting clean process")
    spraytime  = str(float(cleantime.value)/1000)
    cycles = cleancycles.value
    arguments = ["python3","BIUclean.py","--stime",spraytime,"--cycles",cycles]
    #print(arguments)
    #call(arguments)
    Popen(arguments)
    #call(["python3","cleancontrol.py","--stime",stime,"--cycles",cycles])

def pedal():
    GPIO.setup(pin.pedalsensor,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    if button_start.enabled and GPIO.input(pin.pedalsensor)==0:
        print("Pedal triggered")
        startprocess()

def text_box(disp:str, position:list, default):
    '''
    Makes a label+textbox pair

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

    
app = App(title="Back-it-up", layout="grid", width = 600, height = 400)
# Standard Spray
stdlabel            = Text(app, text="Standard Spray", color='white', grid=[0,0,2,1], bg = 'dim gray')
stimelabel, stime   = text_box('Spray time (ms):',       position = [0,1], default = 30)
rdelaylabel, rdelay = text_box('Retraction delay (ms):', position = [0,2], default = 50)
pdelaylabel, pdelay = text_box('Plunge delay (ms):',     position = [0,3], default = 50)
# Pulse Spray
pulselabel  = Text(app, text="(Anti) Pulse Spray", grid=[0,4,2,1], color='white', bg='dim gray')
plen_label, plen   = text_box('Pulse length (ms):',   position = [0,5], default = 16)
pnum_label, pnum   = text_box('Pulse count:',   position = [0,6], default = 5)
pulsenote            = Text(app, text="(Uses retraction & plunge settings from std.)", grid=[0,7,2,1])
## Buttons
button_title = Text(app, text="Triggers", grid=[0,8,2,1], color='white', bg='dim grey')
donotplunge = CheckBox(  app,                       text="Dry fire (do not plunge)?",   grid=[0,9,2,1], align='left')
button_up   = PushButton(app, command=powerup,      text="        Ready        ", grid=[0,10])
button_pulse= PushButton(app, command=startprocess, text="Pulse & Plunge",  grid=[1,10])
button_start= PushButton(app, command=startprocess, text="Spray & Plunge",  grid=[0,11])
button_down = PushButton(app, command=powerdown,    text="         Abort         ",   grid=[1,11], align='left')

button_up.bg="lime green"
button_start.bg = (255, 50, 50)
button_down.bg = "orange"
button_pulse.bg = 'violet'
button_start.disable()
# Cleaning
cleanlabel    = Text(app, text="Cleaning settings:", grid=[2,0,2,1], color='white', bg='dim gray')
cleancycleslabel, cleancycles = text_box('Cleaning cycles:',     position = [2,1], default = 5)
cleantimelabel, cleantime = text_box('Clean pulse length (ms):', position = [2,2], default = 200)
## Buttons
button_clean = PushButton(app, command=cleanprocess, text="        Clean        ", grid=[2,3,2,1])
button_clean.bg = "lightblue"

for element in [button_up, button_start, donotplunge, button_down, button_clean, button_pulse]:
    element.text_size = 12

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
##app.repeat(100,pedal)
app.display()

#shutdown
print('BIU program shutting down...')
powerdown()
GPIO.cleanup()