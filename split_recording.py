from picamera import PiCamera

cam = PiCamera()
cam.start_recording('1.h264')
cam.wait_recording(5)
for i in range(2,5):
  cam.split_recording('%d.h264' % i)
  cam.wait_recording(5)

cam.stop_recording()