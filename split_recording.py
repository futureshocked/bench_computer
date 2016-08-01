# This script shows how to record video in multiple small files
# instead of a single large one.
# Written by Peter Dalmaris for the course Raspberry Pi: Create a Bench Computer

from picamera import PiCamera             # Import the require module

cam = PiCamera()                          # Create the PiCamera object
cam.start_recording('1.h264')             # Start recording video...
cam.wait_recording(5)                     # ... for 5 seconds
for i in range(2,5):                      # ... then create a loop that will create 4 files
  cam.split_recording('%d.h264' % i)      # each file will have a unique name,
  cam.wait_recording(5)                   # and contain 5 seconds of video

cam.stop_recording()                      # stop the video recording
