# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)



# Initialize library.
disp.begin()


# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()



def display(a, b, c, d):

    font = ImageFont.load_default()
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

   

    draw.text((x, top),       a,font=font, fill=255)
    draw.text((x, top+8),     b,font=font, fill=255)
    draw.text((x, top+16),    c,font=font, fill=255)
    draw.text((x, top+25),    d,font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()



def display0(a):
    font = ImageFont.load_default()
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,8), outline=0, fill=0)

    draw.text((x, top),       a,font=font, fill=255)
    
    disp.image(image)
    disp.display()

def display1(b):
    font = ImageFont.load_default()
    # Draw a black filled box to clear the image.
    draw.rectangle((0,8,width,16), outline=0, fill=0)

    draw.text((x, top+8),     b,font=font, fill=255)
   
    disp.image(image)
    disp.display()


def display2(c):
    font = ImageFont.load_default()
    # Draw a black filled box to clear the image.
    draw.rectangle((0,16,width,25), outline=0, fill=0)

   

    # draw.text((x, top),       a,font=font, fill=255)
    # draw.text((x, top+8),     b,font=font, fill=255)
    draw.text((x, top+16),    c,font=font, fill=255)
    # draw.text((x, top+25),    d,font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()

def display3(d):
    font = ImageFont.load_default()
    # Draw a black filled box to clear the image.
    draw.rectangle((0,25,width,32), outline=0, fill=0)

    draw.text((x, top+25),    d,font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()


def clear():

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.display()


if __name__ == '__main__':
    print 'doing the display'
    a = "what's up"
    b = "the custom messge is"
    c = "balls"
    d = "abcdefghijklmnopqrstuv"
    display(a,b,c,d)

