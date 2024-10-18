from picamera2 import Picamera2
import time

camera = Picamera2()
camera.resolution = (1280, 720)
#camera.rotation=180
time.sleep(2)


file_name = "/home/pi/Desktop/image.jpg"
camera.start_and_capture_file(file_name)
print("Done.")
