# You can enter the following commands inside a Python3 command line interpreter,
# or use them in a Python3 script
# Written by Peter Dalmaris for the course Raspberry Pi: Create a Bench Computer

from picamera import PiCamera       # Import the PiCamera module
cam = PiCamera()                    # Create a new PiCamera object
cam.start_recording('/home/pi/Desktop/video_1.h264')     # Record H264 video to the specified location and file name
cam.stop_recording()                # Stops the video recording

# To play back the video file, use omxplayer on the command line:
# omxplayer /home/pi/Desktop/video_1.h264

# To convert a H264 video file to MP4, install and use the MP4Box utility (on the command line again)
# Install:
# sudo apt-get install gpac
# Convert the h264 file into MP4
# MP4Box -add video_1.h264 video_1.mp4    

# Play the new mp4 file with omxplayer
# omxplayer video_1.mp4
# The "blank" switch will hide the desktop while playing back
# omxplayer --blank video_1.mp4


