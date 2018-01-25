#!/usr/bin/python3

''' FILE NAME
relay_demo_gpiod.py
1. WHAT IT DOES
This is a very simple script that shows how to turn on 
and off a single relay on the Keyestudio 4 Channel relay
HAT, or any other relay HAT that can be controled directly
through the Raspberry Pi GPIOs. In this example, the
GPIO is controlled using the pigpio Python module with
the pigpiod (deamon).
 
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
import  pigpio
from time import sleep

pi = pigpio.pi()
relay_a = 22	# Set a GPIO for the realy
pi.set_mode(relay_a,pigpio.OUTPUT)     # Make output

while (True):
	pi.write(relay_a,0)          # Set to LOW
	sleep(1)
	pi.write(relay_a,1)          # Set to HIGH
	sleep(1)