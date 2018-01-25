#!/usr/bin/python3

''' FILE NAME
relay_demo_gpio.py
1. WHAT IT DOES
This is a very simple script that shows how to turn on 
and off a single relay on the Keyestudio 4 Channel relay
HAT, or any other relay HAT that can be controled directly
through the Raspberry Pi GPIOs. In this example, the
GPIO is controlled using the RPi.GPIO Python module.
 
2. REQUIRES
* Any Raspberry Pi with a 40-pin header.
* Keystudio 4 Channel relay HAT or similar

Optional:
* -

3. ORIGINAL WORK
Make A Raspberry Pi Bench Computer, Peter Dalmaris

4. HARDWARE
Connect the required hardware to the Raspberry Pi: Relay HAT.

5. SOFTWARE
* Command line terminal
* Simple text editor
* SSH and SCP
'''

import RPi.GPIO as GPIO
from time import sleep

# The script as below using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set relay pin as output
# For the Keyestudio relay HAT you may also use
# GPIO 4, 6, and 26.
GPIO.setup(22, GPIO.OUT)

while (True): 
    GPIO.output(22, GPIO.HIGH) # Turn ON
    sleep(1)
   
    GPIO.output(22, GPIO.LOW) # Turn OFF
    sleep(1)
