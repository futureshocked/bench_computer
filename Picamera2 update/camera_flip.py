import time
import libcamera
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start_preview(show_preview=True)
preview_config = picam2.create_preview_configuration()
preview_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam2.stop()
picam2.configure(preview_config)
picam2.start()
picam2.capture_file("/home/pi/Desktop/bench_flip.jpg")
picam2.stop_preview()
time.sleep(2)
