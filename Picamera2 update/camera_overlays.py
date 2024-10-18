from picamera2 import Picamera2 
import numpy as np 
picam2 = Picamera2() 
picam2.configure(picam2.create_preview_configuration()) 
picam2.start(show_preview=True) 
overlay = np.zeros((300, 400, 4), dtype=np.uint8) 
overlay[:150, 200:] = (255, 0, 0, 64) # reddish 
overlay[150:, :200] = (0, 255, 0, 64) # greenish 
overlay[150:, 200:] = (0, 0, 255, 64) # blueish 
picam2.set_overlay(overlay)
