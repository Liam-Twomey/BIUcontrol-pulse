from guizero import App, TextBox, Text, PushButton, CheckBox
from subprocess import call, Popen


def startprocess(stime, rdelay, pdelay, is_dry_fire:bool):
    '''
    This function takes in spraytime, retraction delay, and plunge delay to run BIUA&P in the system command line.
    :return: void
    '''
    print("Starting continous spray process.")
    spraytime        = str(float(stime.value)/1000)
    retractiondelay  = str(float(rdelay.value)/1000)
    plungedelay      = str(float(pdelay.value)/1000)
    arguments = ["python3","BIUapplyandplunge.py","--pulse",'False',"--stime",spraytime,"--rdelay",retractiondelay,"--pdelay",plungedelay]
    if is_dry_fire:
        arguments.append("--donotplunge")
    call(arguments)
    
def powerup(tobe_enabled_buttons_list):
    print("Power up")
    arguments = ["python3","BIUpowerupdown.py","--updown","up"]
    call(arguments)
    try:
        for button in tobe_enabled_buttons_list:
            button.enable()
    except:
        return
    
def powerdown(tobe_disabled_buttons_list):
    print("Power down")
    arguments = ["python3","BIUpowerupdown.py","--updown","down"]
    call(arguments)
    try:
        for button in tobe_disabled_buttons_list:
            button.disable()
    except:
        return
    
def pulsestartprocess(rdelay, pdelay, plen, is_dry_fire):
    print("Starting pulse spray.")
    retractiondelay  = str(float(rdelay.value)/1000)
    plungedelay      = str(float(pdelay.value)/1000)
    pulselength       = str(float(plen.value)/1000)
    arguments = ["python3","BIUapplyandplunge.py","--pulse",'True',"--pcycles",pnum.value,"--stime",pulselength, "--breaktime", pinterval, "--rdelay",retractiondelay,"--pdelay",plungedelay]
    if (is_dry_fire):
        arguments.append("--donotplunge")
    call(arguments)

def cleanprocess(cleantime, cleancycles):
    print("Starting clean process")
    spraytime  = str(float(cleantime.value)/1000)
    cycles = cleancycles.value
    arguments = ["python3","BIUclean.py","--stime",spraytime,"--cycles",cycles]
    #print(arguments)
    #call(arguments)
    Popen(arguments)
    #call(["python3","cleancontrol.py","--stime",stime,"--cycles",cycles])