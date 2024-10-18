from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time

camera = Picamera2()
video_config = camera.create_video_configuration()
camera.configure(video_config)

encoder = H264Encoder(bitrate=10000000)
output = "/home/pi/Desktop/video.h264"

camera.start_recording(encoder, output)
time.sleep(10)
camera.stop_recording()

print("Done.")
