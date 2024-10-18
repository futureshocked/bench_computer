import os
from picamera2 import Picamera2, Preview
import time

FOLDER_NAME="/home/pi/camera_activity"

if not os.path.exists(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)


camera = Picamera2()
camera.start_preview(Preview.NULL)
camera.resolution = (1280, 720)
camera.rotation=180
time.sleep(2)

counter =1

while True:
    file_name = FOLDER_NAME + "/img" + str(counter) +".jpg"
    counter += 1
    camera.start_and_capture_file(file_name)
    time.sleep(10)
print("Done.")
