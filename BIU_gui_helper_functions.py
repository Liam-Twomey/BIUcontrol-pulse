from guizero import App, TextBox, Text, PushButton, CheckBox
from subprocess import call, Popen
from pathlib import Path
from datetime import datetime as dtm
from datetime import date as dt

def text_box(app, disp:str, position:list, default):
    '''
    Takes in app as guizero application object, and then return the following to the caller of this function:
        label: a guizero Text object
        box : a guizero TextBox object
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

# def pedal():
#     GPIO.setup(pin.pedalsensor,GPIO.IN, pull_up_down = GPIO.PUD_UP)
#     if button_start.enabled and GPIO.input(pin.pedalsensor)==0:
#         print("Pedal triggered")
#         startprocess()

def startprocess(stime, rdelay, pdelay, is_dry_fire:bool, sprayname, recfile) -> None:
    '''
    This function takes in spraytime, retraction delay, and plunge delay to run BIUA&P in the system command line.
    :return: void
    '''
    print("Starting continous spray process.")
    spraytime        = str(float(stime.value)/1000)
    retractiondelay  = str(float(rdelay.value)/1000)
    plungedelay      = str(float(pdelay.value)/1000)
    print('Starting A&P')
    arguments = ["python3","BIUapplyandplunge.py","--stime",spraytime,"--rdelay",retractiondelay,"--pdelay",plungedelay]
    #button_start.disable()
    if is_dry_fire:
        arguments.append("--donotplunge")
    call(arguments)

    print("A&P finished.")

def pulsestartprocess(rdelay, pdelay, pnum, plen, pinterval, is_dry_fire, sprayname, recfile) -> None:
    '''
    This function takes in retraction delay, plunge delay, and pulse length to run BIUA&P in the system command line.
    :param rdelay: retraction delay
    :param pdelay: plunge delay
    :param plen: pulse length
    :param is_dry_fire: boolean to determine whether to plunge or not
    :return: void
    '''
    print("Starting pulse spray.")
    retractiondelay  = str(float(rdelay.value)/1000)
    plungedelay      = str(float(pdelay.value)/1000)
    pulselength      = str(float(plen.value)/1000)
    breaktime        = str(float(pinterval.value)/1000)
    arguments = ["python3","BIUapplyandplunge.py","--pulse","--pcycles",pnum.value,"--stime",pulselength, "--breaktime", breaktime, "--rdelay",retractiondelay,"--pdelay",plungedelay]
    #button_pulse.disable()
    if (is_dry_fire):
        arguments.append("--donotplunge")
    call(arguments)
    # write records to file
    with open(Path(recfile),'w') as file:
        timestamp = dtm.now().strftime("%d.%b %Y %H:%M:%S")
        lines = ['/n__________',timestamp+' | '+ sprayname,' | Pulse Mode',
        '\tRetraction Delay: '+retractiondelay+' s',
        '\tPlunge Delay: '+plungedelay+' s',
        '\t Pulse Length: '+pulselength+' s',
        '\t Pulse Interval: '+breaktime+' s']
        file.writelines(lines)
        
    

def powerup(tobe_enabled_buttons_list):
    '''
    This function runs BIUpowerupdown.py in the system command line and then takes in a list of buttons to be enabled.
    :param tobe_enabled_buttons_list: list of guizero.PushButton objects to be enabled
    :return: void
    '''
    print("Power up")
    arguments = ["python3","BIUpowerupdown.py","--updown","up"]
    call(arguments)
    try:
        for button in tobe_enabled_buttons_list:
            button.enable()
    except:
        return
    
def powerdown(tobe_disabled_buttons_list):
    '''
    This function runs BIUpowerupdown.py in the system command line and then takes in a list of buttons to be disabled.
    :param tobe_disabled_buttons_list: list of guizero.PushButton objects to be disabled
    :return: void
    '''
    print("Power down")
    arguments = ["python3","BIUpowerupdown.py","--updown","down"]
    call(arguments)
    try:
        for button in tobe_disabled_buttons_list:
            button.disable()
    except:
        return

def cleanprocess(cleantime, cleancycles):
    '''
    This function takes in clean time and clean cycles to run BIUclean.py in the system command line.
    :param cleantime: spray time for cleaning in [ms]
    :param cleancycles: number of cleaning cycles
    :return: void
    '''
    print("Starting clean process")
    spraytime  = str(float(cleantime.value)/1000)
    cycles = cleancycles.value
    arguments = ["python3","BIUclean.py","--stime",spraytime,"--cycles",cycles]
    #print(arguments)
    #call(arguments)
    Popen(arguments)
    #call(["python3","cleancontrol.py","--stime",stime,"--cycles",cycles])
