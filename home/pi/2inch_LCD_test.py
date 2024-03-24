#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont


# From https://www.waveshare.com/wiki/2inch_LCD_Module#Download_Examples
# Wiring matches that of the website above

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't creation of multiple displayer objects!!! '''
    #disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)

    
    # argv code from https://realpython.com/python-command-line-arguments/#displaying-arguments
    logging.info("show image " + sys.argv[1])
    # Loads the file from the command-line
    image = Image.open(sys.argv[1])
    image = image.rotate(180)
    disp.ShowImage(image)
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)

secs = 5
# If there is a second argument in the command-line that is used as the show time.
# If there isn't or if it isn't a number then it crashes and the time is left at 5 seconds.
try:
    secs = int(sys.argv[2])
except:
    print("Using default time")

# This is how long the image shows on the screen. After the program closes the screen goes off.
time.sleep(secs)
