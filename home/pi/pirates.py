import RPi.GPIO as GPIO
import time, sys
import subprocess

subprocess.run(['python 2inch_LCD_test.py start.jpg 5'], shell=True)

from time import sleep
import subprocess
import os
import glob
print("Starting")
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
def temperature():
    print("Getting temperature\n")
    c = read_temp()
    print("Temperature is: " + str(c))
    if c > 25:
        subprocess.run(['python 2inch_LCD_test.py fire.jpg 2'], shell=True)
    else:
        subprocess.run(['python 2inch_LCD_test.py cold.jpg 2'], shell=True)





FLOW_SENSOR_GPIO = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)


GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)


total = 0

global count
count = 0

def countPulse(channel):
  global count
  if start_counter == 1:
     count = count + 1

GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)
old_time = int(time.time())
while True:
    try:
        #happens all the time
        start_counter = 1
        if int(time.time()) > old_time:
            old_time = time.time()
            start_counter = 0
            flow = count
            print("The flow is: " + str(flow))
            if flow > 0:
                total = total + 1
            count = 0
            print("The total is: " + str(total))
           
        #happens only when a button is pressed
        input_state = GPIO.input(21)
        if input_state == False:
            print('Button Pressed')
            if total < 2:
                subprocess.run(['python 2inch_LCD_test.py bad.jpg 1'], shell=True)
            elif total < 5:
                subprocess.run(['python 2inch_LCD_test.py ok.jpg 1'], shell=True)
            else:
                subprocess.run(['python 2inch_LCD_test.py good.jpg 1'], shell=True)
            #also happens when a button ispressed based on temperature
            temperature()
            print("Done")
    except:
       print("Error")
       pass
       
