from picamera2 import Picamera2
from picamera2.encoders import Quality
import time
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size":(1280,720)})
picam2.start_and_record_video("/home/pi/Desktop/test.h264",quality=Quality.HIGH,config=video_config, duration=5, show_preview=True,audio=False)
time.sleep(10)
