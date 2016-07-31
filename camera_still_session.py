# You can enter the following commands inside a Python3 command line interpreter,
# or use them in a Python3 script
# Written by Peter Dalmaris for the course Raspberry Pi: Create a Bench Computer

from picamera import PiCamera       # Import the PiCamera module
cam = PiCamera()                    # Create a new PiCamera object
cam.start_preview()                 # Show a preview 
cam.start_preview(alpha=150)        # Show a preview with alpha for transparency at 150 (valid values 0..255)
cam.stop_preview()                  # Stop a preview
cam.rotation = 180                  # Rotate preview and still image by 180 degrees
cam.start_preview()                 # Show the preview with the rotation set in the previous line
cam.stop_preview()
cam.rotation = 0                    # Rotation back to default
cam.capture('/home/pi/Desktop/bench.jpg')  # Take an image and store it in the prescribed directory and file name
cam.resolution                      # Get the current resolution settings
cam.resolution=(1280,720)           # Set a new resolution
cam.capture('/home/pi/Desktop/bench2.jpg')  # Take an image at the last set resolution
cam.capture('/home/pi/Desktop/bench2.jpg', resize=(800,480))   # Take an image at the last set resolution, then resize it

# Other things you can do with your camera...
cam.sharpness = 0
cam.contrast = 0
cam.brightness = 50
cam.saturation = 0
cam.ISO = 0
cam.video_stabilization = False
cam.exposure_compensation = 0
cam.exposure_mode = 'auto'
cam.meter_mode = 'average'
cam.awb_mode = 'auto'
cam.image_effect = 'none'
cam.color_effects = None
cam.rotation = 0
cam.hflip = False
cam.vflip = False
cam.crop = (0.0, 0.0, 1.0, 1.0)
