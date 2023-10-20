#!/usr/bin/env python3
from guizero import App, TextBox, Text, PushButton, CheckBox
import numpy as np
#from pprint import PrettyPrinter as pp
import BIUpinlist as pin
import gpio as GPIO

def gpio_toggle(pin):
    if type(pin)==int:
        state = GPIO.input(pin)
        if state:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)
        print('int')
    else:
        print(pin, 'is not a gpio pin.')
        return
if __name__=='__main__':
app = App(title="GPIO Tester", layout="grid", width = 600, height = 340)
col1 = np.array(['3V',2,3,4,'G', 17,27,22,'3V',10,9,11,'G',0,5,6,13,19,26,'G'], dtype='object')
col2 = np.array(['5V','5V','G',14,15,18,'G',23,24,'G',25,8,7,1,'G',12,'G',16,20,21], dtype='object')
gpio_labels = np.column_stack((col1, col2))
gpio_buttons = np.empty((20,2), dtype='object')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setmode(BPIO.BCM)
for p in pin:
    GPIO.setup(p,GPIO.OUT)

for i in range(20):
    for j in range(2):
        gpio_buttons[i,j]= PushButton(master=app, text=gpio_labels[i,j], grid=[i,j], align='left', command=gpio_toggle, args=[gpio_labels[i,j]])
        # if type(gpio_labels[i,j] != int):
        #     gpio_buttons[i,j].disable()
            #print(i,' ',j,' ',type(gpio_labels[i,j]))
        #else:
        gpio_buttons[i,j].enable()
#print(gpio_buttons)
app.display()