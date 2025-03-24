import RPi.GPIO as GPIO
import time, sys
import subprocess

# From https://docs.python.org/3.5/library/subprocess.html#subprocess.run
# Runs the edited example screen Python file and shows the logo on it
subprocess.run(['python 2inch_LCD_test.py start.jpg 5'], shell=True)


from time import sleep
import subprocess
import os
import glob
print("Starting")


# From https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
# The reads from the system device to find the temperature from the probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


# Reads the data from the file
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


# Gets a number from the data read from the file
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


# Depending on the temperature being above or below 25c it shows a flame or snowflake
# A larger range of images can be shown for different temperature ranges, but this is just for testing
def temperature():
    print("Getting temperature\n")
    c = read_temp()
    print("Temperature is: " + str(c))
    if c > 25:
        subprocess.run(['python 2inch_LCD_test.py fire.jpg 2'], shell=True)
    else:
        subprocess.run(['python 2inch_LCD_test.py cold.jpg 2'], shell=True)


# From https://www.dfrobot.com/forum/topic/317058
# Sets up the pin the flow meter is plugged into
FLOW_SENSOR_GPIO = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# This is the pin the button is plugged into.
# From http://razzpisampler.oreilly.com/ch07.html
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Used to count how many times they have drunk since the Pi restarted
total = 0


# Counts the numebr of pulses per second
global count
count = 0


# Run whenever the flow meter sends a pulse
def countPulse(channel):
  global count
  if start_counter == 1:
     count = count + 1


# Telling the Rasperry Pi what to do when the flow meter sends a pulse
GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)


# From https://www.influxdata.com/blog/what-is-time-library-in-python-helpful-guide/
# The original code used time.sleep. But the button press didn't work during the sleep.
# Instead it just keeps checking to see if the time has been over a second.
old_time = int(time.time())


# Monitor the flow rate all the time and listen to button presses
while True:
    # If it crashes, it will just try again
    try:
        start_counter = 1
        # Used instead of time.sleep to reset the 1 second flow counter
        if int(time.time()) > old_time:
            old_time = time.time()
            start_counter = 0
            flow = count
            print("The flow is: " + str(flow))
            # Avery second the user drinks the total is increased by 1
            if flow > 0:
                total = total + 1
            count = 0
            print("The total is: " + str(total))

        #happens only when a button is pressed
        input_state = GPIO.input(21)
        if input_state == False:
            print('Button Pressed')
            # For the prototype, you don't need to drink much to change from a thumbs down to an OK
            if total < 2:
                subprocess.run(['python 2inch_LCD_test.py bad.jpg 1'], shell=True)
            elif total < 5:
                subprocess.run(['python 2inch_LCD_test.py ok.jpg 1'], shell=True)
            else:
                # 5 or more seconds drinking means you've drunk enough for the day
                subprocess.run(['python 2inch_LCD_test.py good.jpg 1'], shell=True)
            # Also happens when a button is pressed based on temperature
            temperature()
            print("Done")
    except:
       print("Error")
       pass
       
