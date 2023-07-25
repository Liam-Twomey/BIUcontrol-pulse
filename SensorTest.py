import RPi.GPIO as GPIO
import BIUpinlist as pin

pins = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,8,7,12,16,20,21]#[13,19,26,16,20]

def hi(pinnum):
    GPIO.output(pinnum,GPIO.HIGH)
def lo(pinnum):
    GPIO.output(pinnum,GPIO.LOW)
def reset():
    GPIO.cleanup()
def init():
    GPIO.setmode(GPIO.BCM)
    for i in pins:
        GPIO.setup(i,GPIO.OUT)
init()
