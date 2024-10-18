from picamera2 import Picamera2

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size":(960,540)})
picam2.configure(video_config)

picam2.start_and_record_video("/home/pi/Desktop/test_video.mp4", duration=5)
