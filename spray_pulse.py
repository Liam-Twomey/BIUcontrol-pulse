import RPi.GPIO as GPIO
import time, threading
import argparse
import sys, select
import BIUpinlist as pin

#gpio output pin
pulseLen = 0.016 # s, length of DC pulse to sprayer
pulseSep= 0.005 # s, length of seperation between pulses
numPulse = 5 # number of pulses

if __name__=='__main__':

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin.cannon,GPIO.OUT)

    parser = argparse.ArgumentParser(description='Arguments for sample pulse')
    parser.add_argument('--ptime', help='Duration of application pulse (seconds)', default = pulseLen, type=float,required=False)
    parser.add_argument('--pcycles', help='number of application pulses',default = numPulse, type=int,required=False)
    parser.add_argument('--breaktime', help='Pause between application pulses (seconds)',default = pulseSep, type=int,required=False)
    pulseArgs = parser.parse_args()

    for x in range(pulseArgs.cycles):
        GPIO.output(pin.cannon,GPIO.HIGH)
        time.sleep(pulseArgs.stime)
        GPIO.output(pin.cannon,GPIO.LOW)
        time.sleep(0.2)
    
GPIO.cleanup()