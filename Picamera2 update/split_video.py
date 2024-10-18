from picamera2 import Picamera2
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size":(960,540)})
picam2.configure(video_config)
startfilename = "video"
ctr = 0

# Loop to create new videos every 5 seconds
while True:
    ctr=ctr+1
    filename= startfilename + str(ctr)	
    picam2.start_and_record_video("/home/pi/Desktop/" + filename + ".mp4", duration=5)

