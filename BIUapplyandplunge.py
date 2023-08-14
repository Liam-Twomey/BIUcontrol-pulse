#!/usr/bin/env python3

# Uncomment for use of pi
import RPi.GPIO as GPIO # For RPi
#import gpio as GPIO # Testing on Linux/Mac
#import Adafruit_DHT
import time, threading
import argparse
import sys, select
import BIUpinlist as pin

def filterforward(filterposition):
    '''
    :param filterposition: name of pin on RPi for filter paper
    :return: void
    '''
    print("Advancing the cannon")
    GPIO.output(filterposition,GPIO.HIGH)

def powerupsensors(sensorpower):
    '''
    :param sensorpower: name of pin on RPi for powering up the sensor
    :return: void
    '''
    GPIO.output(sensorpower,GPIO.HIGH)

def powerdownsensors(sensorpower):
    '''
    :param sensorpower: name of pin on RPi for powering down the sensor
    :return: void
    '''
    GPIO.output(sensorpower,GPIO.LOW)
    
def filterreverse(filterposition,filterreversedelay):
    '''
    :param filterposition: pin name associated in positioning the filter
    :param filterreversedelay: time delay to reverse the filter
    :return: void
    '''
    time.sleep(filterreversedelay)
    print("Reversing the filter")
    GPIO.output(filterposition,GPIO.LOW)

def applysample(pin_cannon, duration:int):
    '''
    :param pin_cannon: pin name associated with the positioning solenoid
    :param duration: time duration [ms]
    :return: void
    '''
    GPIO.output(pin_cannon, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin_cannon, GPIO.LOW)
def pulseapplysample(pin_cannon, cycles:int, ptime:int, pbreak):
    '''
    :param pin_cannon:pin name associated with the positioning solenoid
    :param cycles: number of sample application pulses
    :param ptime: pulse time in [ms]
    :param pbreak: pause between sample application pulses [s]
    :return: void
    '''
    for x in range(int(cycles)):
        GPIO.output(pin_cannon, GPIO.HIGH)
        time.sleep(ptime)
        GPIO.output(pin_cannon, GPIO.LOW)
        time.sleep(pbreak)
    return
    
def releaseplunger(plunger,wait):
    time.sleep(wait)
    print("Releasing the plunger")
    GPIO.output(plunger,GPIO.HIGH)

def resetplunger(plunger):
    GPIO.output(plunger,GPIO.LOW)
    
'''def readenvironment(dht22):
    humidity, temperature = Adafruit_DHT.read_retry(22, pin=dht22)
    return humidity, temperature
''' 

if __name__=='__main__':
    #Read flags from CLI input, store in args
    parser = argparse.ArgumentParser(description='Arguments for BIUcontrol')
    parser.add_argument('--stime',      help='Duration of sample application or pulse (seconds)',type=float,required=True)
    parser.add_argument('--rdelay',     help='Time to wait before retracting filter (seconds)',default = 0, type=float,required=False)
    parser.add_argument('--pdelay',     help='Time to wait before plunging (seconds)',default = 0, type=float,required=False)
    parser.add_argument('--donotplunge',help='Do not fire the plunger (diagnostic)',action = 'store_true')  
    parser.add_argument('--pulse', help='Choose whether to spray continuously (False) or pulse (True)', type=bool, default=False)
    # Clean me up!
    parser.add_argument('--pcycles', help='number of application pulses',default = 1, type=int,required=False)
    parser.add_argument('--breaktime', help='Pause between application pulses (seconds)',default = 50, type=int,required=False)
    args = parser.parse_args()
    
    # Default timing
    #cannontimetoreverse = 0.020
    #cannonreversedelay  = args.stime + args.sdelay+ cannontimetoreverse

    #Setup GPIO for appropriate I/O
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin.cannon,GPIO.OUT)
    GPIO.setup(pin.plunger,GPIO.OUT)
    GPIO.setup(pin.filterposition,GPIO.OUT)
    GPIO.setup(pin.sensorpower,GPIO.OUT)
    #GPIO.setup(pin.pedalsensor,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(pin.interlock,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        
    # Report environmental conditions -- not yet implemented
#    humidity, temperature = readenvironment(pin.dht22)
#    print('Temp={0:0.1f}\'C  Humidity={1:0.1f}% RH'.format(temperature, humidity))

    # Print out initial conditions and inputs to terminal
    print("Timings:")
    print("Specimen application will start at time: 0")
    print("Specimen application will end at time: ",args.stime)
    print("Filter will retract at time: ",args.rdelay)
    print("Plunger will fall at time: ",args.pdelay)
    kuhnketime = 1 # time for which plunger is energized to plunge
    energizedtime = kuhnketime+max(args.pdelay,args.stime,args.rdelay)
    print("Plunger will remain energized until: ",energizedtime)
    print("Program will exit after: ",1+energizedtime)
    #if cannonreversedelay > args.pdelay:
    #    print("The cannon does not have sufficient time to reverse before plunging!!")
    #    exit()

    # Check interlock -- not currently functional
    '''if GPIO.input(pin.interlock)==1:
        print("Interlock fail: cryogen container is not in place")
        powerdownsensors(pin.sensorpower)
        filterreverse(pin.filterposition,0)
        exit()
    else:
        print("Safety interlock pass: cryogen container is in place")
    '''
    # Setup threads so each major physical movement runs on a seperate process
    sample_thread = threading.Thread(target=applysample, args=(pin.cannon, args.stime))
    filterposition_thread = threading.Thread(target=filterreverse, args=(pin.filterposition, args.rdelay))
    plunger_thread = threading.Thread(target=releaseplunger, args=(pin.plunger, args.pdelay))
    pulse_thread = threading.Thread(target=pulseapplysample, args=(pin.cannon, args.pcycles, args.stime, args.breaktime))
    
    # Initialize all threads
    if not args.donotplunge:
        plunger_thread.start()
    if (args.pulse == True):
        pulse_thread.start()
    elif (args.pulse == False):
        sample_thread.start()
    else:
        print('Error: args.pulse is undefined.')

    filterposition_thread.start()
    
    # Kuhnke (big) plunger -- plunge and reset circuit
    time.sleep(kuhnketime+args.pdelay)
    resetplunger(pin.plunger)
    if max(args.stime,args.pdelay,args.rdelay) != args.pdelay:
        time.sleep(1+max(args.stime,args.rdelay)-args.pdelay)
    powerdownsensors(pin.sensorpower)

    #GPIO.cleanup()
    print("Done!")

