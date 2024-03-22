from time import sleep
import subprocess
sleep(1)
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
while True:
    temperature()
    sleep(1)
