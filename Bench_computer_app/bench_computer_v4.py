#!/usr/bin/python3

''' FILE NAME
bench_control.py
1. WHAT IT DOES
This is a GUI application that runs on any Raspberry Pi with a 40-pin header. 
It requires a Piface Realy Plus HAT

This version of the app implements the Environment tab (Tab 3)
 
2. REQUIRES
* Any Raspberry Pi with a 40-pin header.
* Piface Realy Plus HAT
* Rapsberry Pi camera
* Raspberry Pi 7-inch touch screen
* Case

Optional:
* A 5mm LED
* A 5V-10A relay
* A 220Ohm resistor
* Jumper wires

3. ORIGINAL WORK
Make A Raspberry Pi powered bench computer, Peter Dalmaris

4. HARDWARE
Connect the required hardware to the Raspberry Pi: touch screen, Piface Relay Plus HAT, camera.

Connect the external devices you wish to control to the relay terminals.

5. SOFTWARE
* Command line terminal
* Simple text editor
* SSH and SCP
'''


from    tkinter     import *
from    tkinter.ttk import *
from    tkinter     import messagebox

# Used with the bench control functions
import  pifacerelayplus

# Used with the camera functions
import  picamera
import  PIL
from    PIL         import ImageTk
from    PIL         import Image
import  datetime                      # used to create a unique file name for each image
import  os

# Used with the environment functions
import  pigpio
import  DHT22
import  Adafruit_DHT
from    time        import sleep, strftime

PROGRAM_NAME          = "Tech Explorations Bench Controller"
IMAGE_FILE_LOCATION   = "../photos"
VIDEO_FILE_LOCATION   = "../videos"
DHT_SENSOR_PIN        = 4
DHT_SENSOR_TYPE       = 2302
DHT_FREQUENCY         = 10000


class BenchComputer(Frame):

  def __init__(self, root):
    Frame.__init__(self, root)   

    self.pfr = pifacerelayplus.PiFaceRelayPlus(pifacerelayplus.RELAY)
    self.pfr.init_board(  {   'value':      0, 
                              'direction':  0, 
                              'pullup':     0}, 
                          {   'value':      0, 
                              'direction':  0,    # Makes all pins outputs outputs
                              'pullup':     0})   

    root.protocol("WM_DELETE_WINDOW", self.on_closing)  # This will create a pop-up to confirm ending the program, and
                                                        # if there is confirmation it will call the on_closing method
                                                        # to tidy up before closing.
    # Bench control, Tab 1, variables
    self.lightOnImage                           = PhotoImage(file="icons/light-bulb.png")    
    self.fanImage                               = PhotoImage(file="icons/ac.png")
    self.ironImage                              = PhotoImage(file="icons/iron-soldering.png")
    self.gpioONImage                            = PhotoImage(file="icons/switch.png")
    self.gpioOFFImage                           = PhotoImage(file="icons/switch-2.png")
    self.hairdryerImage                         = PhotoImage(file="icons/hairdryer.png")                                                        

    # Camera, Tab 2 variables
    self.camera                                 = picamera.PiCamera()    
    self.last_photo                             = None    #declaring without defining.
    self.isVideoRecording                       = FALSE
    self.isTakingIntervalPhotos                 = FALSE
    self.intervalStillButtonPressed             = FALSE
    self.intervalImageCounter                   = 0
    self.photoInterval                          = 5     # interval in seconds.
    self.directory_interval                     = None
    self.file_name_interval                     = None 
    self.intervalCamera                         = PhotoImage(file="icons/multiple-shots.png")
    self.videoCamera                            = PhotoImage(file="icons/video-camera.png")  
    self.add                                    = PhotoImage(file="icons/add.png")         
    self.remove                                 = PhotoImage(file="icons/minus.png") 
    self.stillCamera                            = PhotoImage(file="icons/photo-camera.png")  

    # Environment, Tab 3 variables
    self.pi                                     = pigpio.pi()
    self.sensor                                 = DHT22.sensor(self.pi, DHT_SENSOR_PIN)
    self.clock                                  = PhotoImage(file="icons/clock.png") 
    self.humidity                               = PhotoImage(file="icons/humidity.png")         
    self.thermometer                            = PhotoImage(file="icons/thermometer.png")           



    self.pack(fill=BOTH,expand=True)
    self.root = root
    self.root.title(PROGRAM_NAME)
    self.initUI()

  def initUI(self):
    self.root.update()   #I call update in order to draw the root window so that I can take its dimensions
                         # in the next line.

    # Create the notebook with three tabs
    style   = Style()
    mygreen = "#d2ffd2"
    myred   = "#dd0202"

    style.theme_create(   "benchComputer", 
                          parent="alt", 
                          settings={
                                      "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
                                      "TNotebook.Tab": {
                                      "configure": {"padding": [10, 10], "background": mygreen },
                                      "map":       {"background": [("selected", myred)],
                                      "expand": [("selected", [1, 1, 1, 0])] } } } )

    style.theme_use("benchComputer")

    ##############################################################
    # You can also customise the theme for each frame, like this:
    # s = Style()
    # s.configure('Tab1.TFrame', background='cyan')
    # s.configure('Tab2.TFrame', background='red')
    # s.configure('Tab3.TFrame', background='magenta')
    
    # frame1 = Frame(width=400, height=300, style='Tab1.TFrame')
    # frame2 = Frame(width=400, height=300, style='Tab2.TFrame')
    # frame3 = Frame(width=400, height=300, style='Tab3.TFrame')
    ##############################################################

    # Create the notebook UI
    notebook  = Notebook(  self,
                          height  = self.root.winfo_height(),
                          width   = self.root.winfo_width()-150,
                          style   = "large.TNotebook")
    frame1    = Frame() 
    frame2    = Frame() 
    frame3    = Frame()

    notebook.add(frame1,text  = "Instruments") 
    notebook.add(frame2,text  = "Camera") 
    notebook.add(frame3,text  = "Environment") 
    notebook.pack(pady = 5, side = LEFT)

    

    #Create the log text area    
    log_label                                     = Label(self,text="Log")
    log_label.configure(  background              = "white", 
                          width                   = 150, 
                          justify                 = CENTER, 
                          font                    = ("Helvetica", 14))
    log_label.pack(       side                    = TOP)
    self.log_textBox    = Text( self,             
                                height  = self.root.winfo_height(),               
                                width   = 150)
    self.log_textBox.pack(      side    = RIGHT)

    #Styles
    buttonStyle                               = Style()
    buttonStyle.configure(  "Normal.TButton", 
                            background        = "#91C497", 
                            borderwidth       = 1, 
                            activeforeground  = "#30903C", 
                            compound          = "BOTTOM")
    buttonStyle.configure(  "Selected.TButton", 
                            background        = "#107B1D", 
                            borderwidth       = 1, 
                            activeforeground  = "#30903C", 
                            compound          = "BOTTOM")
    buttonStyle.configure(  "TextOnly.TButton", 
                            borderwidth       = 1, 
                            activeforeground  = "#30903C", 
                            font              = ('Helvetica', '40'), 
                            padding           = (0, 0, 0, 0), 
                            width             = 3, 
                            height            = 3)
    
    #Styles for the camera and environment tabs
    intervalLabelStyle                        = Style()
    intervalLabelStyle.configure(     "IntervalLabel.TLabel",
                                      font        = ('Helvetica', '18'),
                                      padding     = (0, 0, 0, 0), 
                                      justify     = LEFT)
    intervalLabelStyle.configure(     "Enrironment.TLabel",
                                      font        = ('Helvetica', '70'),
                                      padding     = (0, 0, 0, 0), 
                                      justify     = LEFT)
    intervalLabelStyle.configure(     "EnrironmentTime.TLabel",
                                      font        = ('Helvetica', '30'),
                                      padding     = (0, 10, 0, 0), 
                                      justify     = LEFT)

    cameraInfoLabelStyle                          = Style()
    cameraInfoLabelStyle.configure(   "cameraInfoLabel.TLabel",
                                      font        = ('Helvetica', '10'),
                                      padding     = (0, 0, 0, 0), 
                                      justify     = LEFT)

    # Create the UI in the Instruments tab (frame1)
    Style().configure(          "TButton", 
                                padding   = (30, 30, 30, 30), 
                                font      = 'serif 10')  # Applies to all buttons
    
    frame1.columnconfigure(     0, pad    = 3)
    frame1.columnconfigure(     1, pad    = 3)
    frame1.columnconfigure(     2, pad    = 3)
    frame1.rowconfigure(        0, pad    = 3) 
    frame1.rowconfigure(        1, pad    = 3) 
    frame1.rowconfigure(        2, pad    = 3)
    self.lights1_button   = Button(   frame1,           
                                      text      = "Lights 1",          
                                      command   = self.relay1Toggle,  
                                      image     = self.lightOnImage,
                                      style     = "Normal.TButton")    
    self.lights1_button.grid(         row       = 0, 
                                      column    = 0)
    self.extractor_button = Button(   frame1,           
                                      text      = "Extractor",         
                                      command   = self.toggleFan,  
                                      image     = self.fanImage,
                                      style     = "Normal.TButton")    
    self.extractor_button.grid(       row       = 0, 
                                      column    = 1)
    self.solder_button    = Button(   frame1,           
                                      text      = "solder",            
                                      command   = self.bigRelay1,  
                                      image     = self.ironImage,
                                      style     = "Normal.TButton")    
    self.solder_button.grid(          row       = 0, 
                                      column    = 2)
    self.hotairgun_button = Button(   frame1,           
                                      text      = "Hot air gun",            
                                      command   = self.bigRelay2,  
                                      image     = self.hairdryerImage,
                                      style     = "Normal.TButton")    
    self.hotairgun_button.grid(       row       = 1, 
                                      column    = 0)
    self.io2_button       = Button(   frame1,           
                                      text      = "GPIO 2",            
                                      # command   = self.bigRelay2,  
                                      image     = self.gpioONImage,
                                      style     = "Normal.TButton")    
    self.io2_button.grid(             row       = 1, 
                                      column    = 1)
    self.io3_button       = Button(   frame1,           
                                      text      = "GPIO 3",            
                                      # command   = self.relay1Toggle,  
                                      image     = self.gpioONImage,
                                      style     = "Normal.TButton")
    self.io3_button.grid(             row       = 1, 
                                      column    = 2)

    # Create the UI in the Camera tab (frame2)
    cameraFrameLeft       = Frame(    frame2, 
                                      height    = self.root.winfo_height(),
                                      width     = 150, 
                                      relief    = SUNKEN)
    
    cameraFrameLeft.pack(             pady      = 1,
                                      side      = LEFT)
    
    self.cameraFrameRight = Frame(    frame2, 
                                      height    = self.root.winfo_height(), 
                                      width     = 450, 
                                      relief    = SUNKEN) # This frame will contain the image preview
    self.cameraFrameRight.pack(       pady      = 1,
                                      side      = RIGHT)

    stillPhotoButton          = Button(   cameraFrameLeft,           
                                          text      = "Still",          
                                          command   = self.take_still,  
                                          image     = self.stillCamera,
                                          style     = "Normal.TButton")   

    stillPhotoButton.grid(                row       = 0, 
                                          column    = 0, 
                                          rowspan   = 1)

    intervalPhotoButton       = Button(   cameraFrameLeft,           
                                          text      = "Interval",          
                                          command   = self.startIntervalStill,  
                                          image     = self.intervalCamera,
                                          style     = "Normal.TButton")    

    intervalPhotoButton.grid(             row       = 1, 
                                          column    = 0,  
                                          rowspan   = 1)

    videoButton               = Button(   cameraFrameLeft,           
                                          text      = "Video",          
                                          command   = self.toggleVideo,  
                                          image     = self.videoCamera,
                                          style     = "Normal.TButton")   

    videoButton.grid(                     row       = 4, 
                                          column    = 0,  
                                          rowspan   = 2)


    self.intervalText         = Label(    cameraFrameLeft, 
                                          text      = "Interval: {}s\n".format(self.photoInterval), 
                                          style     = "IntervalLabel.TLabel")    

    increaseInterval          = Button(   cameraFrameLeft, 
                                          text      = "Increase", 
                                          command   = self.increase_photo_interval, 
                                          image     = self.add, 
                                          style     = "Normal.TButton")

    decreaseInterval          = Button(   cameraFrameLeft, 
                                          text      = "Decrease", 
                                          command   = self.decrease_photo_interval, 
                                          image     = self.remove, 
                                          style     = "Normal.TButton")    
    
    self.intervalText.grid(               row         = 0,
                                          column      = 1,
                                          columnspan  = 2,
                                          rowspan     = 1)

    increaseInterval.grid(                row         = 1,
                                          column      = 2)

    decreaseInterval.grid(                row         = 1,
                                          column      = 3)

    self.cameraStatus         = Label(    cameraFrameLeft, 
                                          text        = "NOT RECORDING", 
                                          style       = "cameraInfoLabel.TLabel")

    self.cameraStatus.grid(               row         = 4,
                                          column      = 2,
                                          columnspan  = 2)

    # Create the UI in the Environment tab (frame3)
    temperatureLabel                  = Label(    frame3,                                           
                                                  image     = self.thermometer)   
    humidityLabel                     = Label(    frame3,                                           
                                                  image     = self.humidity)
    timedateLabel                     = Label(    frame3,                                           
                                                  image     = self.clock)

    temperatureLabel.grid(                  row         = 0,
                                            column      = 0)

    humidityLabel.grid(                     row         = 1,
                                            column      = 0)

    timedateLabel.grid(                     row         = 2,
                                            column      = 0)

    self.environmentTimeLabel         = Label(    frame3, 
                                          text        = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                                          style       = "EnrironmentTime.TLabel")
    
    self.environmentTimeLabel.grid(       row         = 2, 
                                          column      = 1,  
                                          columnspan  = 5)
    
    self.temperatureLabel            = Label(    frame3, 
                                          text        = "-", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityLabel               = Label(    frame3, 
                                          text        = "-", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityLabel.grid(              row         = 1, 
                                          column      = 1)

    self.temperatureLabel.grid(           row         = 0, 
                                          column      = 1)
    
    self.temperatureUnitLabel            = Label(    frame3, 
                                          text        = "\u00b0C", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityUnitLabel               = Label(    frame3, 
                                          text        = "%", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityUnitLabel.grid(          row         = 1, 
                                          column      = 2)
    
    self.temperatureUnitLabel.grid(       row         = 0, 
                                          column      = 2)
  # Environment - Tab 3 - methods
  def getDHTreadings(self):
    # Here is how to implement the sensor so that SUDO is not required
    # http://www.rototron.info/dht22-tutorial-for-raspberry-pi/
    # This works ok with Python 3

    self.sensor.trigger()
    sleep(.2) # Necessary on faster Raspberry Pi's BUT I WILL NEED TO FIND A NON-BLOCKING WAY TO DELAY
              # SLEEP SHOULD NOT BE USED IN A GUI APPLICATION!!!

    # To convert Celsius to Farenheit, use this formula: (°C × 9/5) + 32 = °F
    temperature = self.sensor.temperature()
    humidity    = self.sensor.humidity()

    self.temperatureLabel.config(     text  =  "{:3.2f}".format(temperature / 1.))
    self.humidityLabel.config(        text  =  "{:3.2f}".format(humidity / 1.))
    self.environmentTimeLabel.config( text  =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))           # Prints out to the terminal
    print("{:3.2f}, {:3.2f}".format(temperature / 1., humidity / 1.))   # Prints out to the terminal

    self.root.after(DHT_FREQUENCY, self.getDHTreadings)
  
  # Camera - Tab 2 - methods
  def startIntervalStill(self):
    if self.intervalStillButtonPressed == FALSE:
      self.intervalStillButtonPressed   = TRUE
      self.log_textBox.insert(0.0, "Pressed interval photo button. Interval button pressed is TRUE.\n")      
      self.cameraStatus.config(text     = "Taking interval still images...")
      self.takeIntervalStill()
    else:
      self.intervalStillButtonPressed   = FALSE
      self.log_textBox.insert(0.0, "Pressed interval photo button. Interval button pressed is FALSE.\n")
      self.cameraStatus.config(text     = "")

  def takeIntervalStill(self):  
    #This method works like this:
    #Say the interval is set to 5 seconds
    #First, the method is called and the first photo is taken, and shown in the frame.
    #Second, this method is scheduled to be called again using the tkinter 
    #root "after" method, at the set interval, unless the user has cancelled the 
    #interval photo function by pressing the button again.
    if self.isTakingIntervalPhotos == FALSE and self.intervalStillButtonPressed   == TRUE:
      self.directory_interval       = '{}/Interval_{}'.format(IMAGE_FILE_LOCATION, datetime.datetime.now().strftime("%B_%d_%y_%H_%M_%S"))  
      #self.directory_interval       = '../photos/Interval_{}'.format(datetime.datetime.now().strftime("%B_%d_%y_%H_%M_%S"))  
      if not os.path.exists(self.directory_interval):
        os.makedirs(self.directory_interval)
        self.file_name_interval     = '{}/{}.jpg'.format(self.directory_interval,self.intervalImageCounter)  
        self.intervalImageCounter   += 1
        self.log_textBox.insert(0.0, "Taking an image every {} seconds, storing at location {}.\n".format(self.photoInterval,self.directory_interval))
        self.isTakingIntervalPhotos = TRUE
        self.root.after(self.photoInterval, self.takeIntervalStill)
      else:
        self.log_textBox.insert(0.0, "Ended recording interval photos. Total {} taken, stored at location {}.\n".format(self.intervalImageCounter,self.interval))
        self.intervalImageCounter   = 0


    if self.isTakingIntervalPhotos  == TRUE and self.intervalStillButtonPressed   == TRUE:  
      self.intervalImageCounter     += 1 
      self.file_name_interval       = '{}/{}.jpg'.format(self.directory_interval,self.intervalImageCounter)  
      self.camera.capture(self.file_name_interval)
      self.log_textBox.insert(0.0, "Captured interval image {}\n".format(self.file_name_interval))
      image           = Image.open(self.file_name_interval)
      image           = image.resize((350, 210), Image.ANTIALIAS) 
      self.last_photo = ImageTk.PhotoImage(image)
      Label(self.cameraFrameRight, image=self.last_photo).grid(row=0, column=0)
      self.root.after(self.photoInterval*1000, self.takeIntervalStill)


  def toggleVideo(self):
    if self.isVideoRecording  == FALSE:
      self.isVideoRecording   = TRUE      
      file_name               = '{}/{}.h264'.format(VIDEO_FILE_LOCATION,datetime.datetime.now().strftime("%B_%d_%y_%H_%M_%S"))
      self.log_textBox.insert(0.0, "Video is recording: {}\n".format(file_name))
      self.camera.start_recording(file_name)
      self.cameraStatus.config(text="RECORDING...");
    else:
      self.isVideoRecording   = FALSE
      self.log_textBox.insert(0.0, "Video is stopped\n")
      self.camera.stop_recording()
      self.cameraStatus.config(text="NOT RECORDING");

  def increase_photo_interval(self):
    self.photoInterval        += 1
    self.log_textBox.insert(0.0, "Interval: {}s\n".format(self.photoInterval))
    self.intervalText.config(text="Interval: {}s\n".format(self.photoInterval), style="IntervalLabel.TLabel")

  def decrease_photo_interval(self):
    if self.photoInterval > 1:
      self.photoInterval -= 1
    self.log_textBox.insert(0.0, "Interval: {}s\n".format(self.photoInterval))
    self.intervalText.config(text="Interval: {}s\n".format(self.photoInterval), style="IntervalLabel.TLabel")

  def take_still(self):
    self.log_textBox.insert(0.0, "Capturing image...\n")
    file_name = '{}/{}.jpg'.format(IMAGE_FILE_LOCATION,datetime.datetime.now().strftime("%B_%d_%y_%H_%M_%S"))
    self.camera.capture(file_name)
    self.log_textBox.insert(0.0, "Captured image {}\n".format(file_name))

    image           = Image.open(file_name)
    image           = image.resize((360, 216), Image.ANTIALIAS) 
    self.last_photo = ImageTk.PhotoImage(image)
    Label(self.cameraFrameRight, image=self.last_photo).grid(row=0, column=0)

  # Bench control - Tab 1 - methods
  def bigRelay1(self):
    self.pfr.x_pins[2].toggle()
    if self.pfr.x_pins[2].value == 0:
      relay_value = "ON"  
      self.solder_button.config(image=self.ironImage,style="Selected.TButton")
    else: 
      relay_value = "OFF"
      self.solder_button.config(image=self.ironImage,style="Normal.TButton")
    self.log_textBox.insert(0.0, "BigRelay1 is {}\n".format(relay_value))

  def bigRelay2(self):
    self.pfr.x_pins[3].toggle()
    if self.pfr.x_pins[3].value == 0:
      relay_value = "ON"  
      self.hotairgun_button.config(image=self.hairdryerImage,style="Selected.TButton")
    else: 
      relay_value = "OFF"
      self.hotairgun_button.config(image=self.hairdryerImage,style="Normal.TButton")
    self.log_textBox.insert(0.0, "BigRelay0 is {}\n".format(relay_value))

  def toggleFan(self):
      self.pfr.relays[1].toggle()
      
      relay_value   = "ON" 
      if self.pfr.relays[1].value == 1:
        relay_value = "ON"       
        self.extractor_button.config(image=self.fanImage,style="Selected.TButton")  
      else:
        relay_value = "OFF"        
        self.extractor_button.configure(image=self.fanImage,style="Normal.TButton") 

      self.log_textBox.insert(0.0, "Fan is {}\n".format(relay_value))

  def relay1Toggle(self):
    self.pfr.relays[0].toggle()
    if self.pfr.relays[0].value == 1:
      relay_value = "ON" 
      self.lights1_button.config(image=self.lightOnImage,style="Selected.TButton")
    else: 
      relay_value = "OFF"
      self.lights1_button.configure(image=self.lightOnImage,style="Normal.TButton")      

    self.log_textBox.insert(0.0, "Light is {}\n".format(relay_value))

  def on_closing(self):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.pfr.init_board(  {   'value':      0, 
                              'direction':  0, 
                              'pullup':     0}, 
                          {   'value':      0, 
                              'direction':  0,    # Makes all pins outputs outputs
                              'pullup':     0})
        self.root.destroy()

def main():
  root = Tk()
  root.attributes('-zoomed', True)
  ex = BenchComputer(root)
  root.after(DHT_FREQUENCY, ex.getDHTreadings) #This will trigger the first sensor reading
  root.mainloop()  

if __name__ == '__main__':
    main()  
