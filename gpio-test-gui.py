#!/usr/bin/env python3
from guizero import App, CheckBox, Picture
import numpy as np
#from pprint import PrettyPrinter as pp
#import BIUpinlist as pin
import RPi.GPIO as GPIO

def gpio_toggle(i,j):
    pin = gpio_buttons[i,j]
    plab = gpio_labels[i,j]
    if pin.value==1:
        GPIO.output(plab, GPIO.HIGH)
        print(plab, 'is HIGH')
    else:
        GPIO.output(plab, GPIO.LOW)
        print(plab, 'is LOW')
        
app = App(title="GPIO Tester", layout="grid", width = 280, height = 470)
col1 = ['3V',2,3,4,'G', 17,27,22,'3V',10,9,11,'G',0,5,6,13,19,26,'G']
col2 = ['5V','5V','G',14,15,18,'G',23,24,'G',25,8,7,1,'G',12,'G',16,20,21]
gpio_labels = np.column_stack([np.array(col1, dtype='object'), np.array(col2, dtype='object')]).T
gpio_buttons = np.empty((2,20), dtype='object')

pinarr = col1 + col2
pins= [i for i in pinarr if type(i)==int]
print(pins)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
for p in pins:
    GPIO.setup(p,GPIO.OUT)

for i in range(2):
    for j in range(20):
        gpio_buttons[i,j]= CheckBox(master=app, text=gpio_labels[i,j], grid=[i,j], command=gpio_toggle, args=[i,j])
        if type(gpio_labels[i,j]) != int:
            gpio_buttons[i,j].disable()
            #print(i,' ',j,' ',type(gpio_labels[i,j]))
        #else:
        #gpio_buttons[i,j].enable()
pinout = Picture(app, image="pinout.png", grid = [3, 0,1,20])
app.display()
