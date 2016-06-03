#!/usr/bin/python3

# This version of the app is running on Python 3
# I am adding scheduling so I can take interval still images.

# v.8 includes the DHT22 code

from    tkinter     import *
from    tkinter.ttk import *
from    time        import sleep, strftime
import  datetime
import  pifacerelayplus
import  datetime
import  picamera
import  PIL
from    PIL         import ImageTk
from    PIL         import Image
import  os
import  pigpio
import  DHT22


import  Adafruit_DHT

PROGRAM_NAME      = "Tech Explorations Bench Controller"
DHT_SENSOR_PIN    = 4
DHT_SENSOR_TYPE   = 2302
DHT_FREQUENCY     = 10000

class BenchComputer(Frame):

  def __init__(self, root):
    Frame.__init__(self, root)   

    self.pfr = pifacerelayplus.PiFaceRelayPlus(pifacerelayplus.RELAY)
    self.pfr.init_board(  {   'value':      0, 
                              'direction':  0, 
                              'pullup':     0}, 
                          {   'value':      0, 
                              'direction':  0, #Makes X3 an input, and the rest outputs
                              'pullup':     0})  #makes GPIOs outputs

    #Setup the interrupt for the button connected to X3 (GPIO 0)
    # listener = pifacerelayplus.InputEventListener(chip=self.pfr)
    # listener.register(0, pifacerelayplus.IODIR_RISING_EDGE, print)
    # listener.activate()

    self.camera                                 = picamera.PiCamera()
    self.last_photo                             = None    #declaring without defining.
    self.isVideoRecording                       = FALSE
    self.isTakingIntervalPhotos                 = FALSE
    self.intervalStillButtonPressed             = FALSE
    self.intervalImageCounter                   = 0
    self.photoInterval                          = 5     # interval in seconds.
    self.directory_interval                     = None
    self.file_name_interval                     = None 
    self.lightOnImage                           = PhotoImage(file="icons/light-bulb.png")    
    self.fanImage                               = PhotoImage(file="icons/vehicle.png")
    self.ironImage                              = PhotoImage(file="icons/tool.png")
    self.gpioONImage                            = PhotoImage(file="icons/switch-1.png")
    self.gpioOFFImage                           = PhotoImage(file="icons/switch-2.png")
    self.stillCamera                            = PhotoImage(file="icons/CompactCamera-50.png")
    self.intervalCamera                         = PhotoImage(file="icons/StackofPhotos-50.png")
    self.videoCamera                            = PhotoImage(file="icons/VideoCall-50.png")  
    self.add                                    = PhotoImage(file="icons/add-16.png")         
    self.remove                                 = PhotoImage(file="icons/remove-16.png")         
    self.root                                   = root
    self.root.title(PROGRAM_NAME)
    self.pack(fill=BOTH,expand=True)
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

    #Styles
    buttonStyle                               = Style()
    buttonStyle.configure(  "Normal.TButton", 
                            background        = "#91C497", 
                            borderwidth       = 3, 
                            activeforeground  = "#30903C", 
                            compound          = "BOTTOM")
    buttonStyle.configure(  "Selected.TButton", 
                            background        = "#107B1D", 
                            borderwidth       = 3, 
                            activeforeground  = "#30903C", 
                            compound          = "BOTTOM")
    buttonStyle.configure(  "TextOnly.TButton", 
                            borderwidth       = 1, 
                            activeforeground  = "#30903C", 
                            font              = ('Helvetica', '40'), 
                            padding           = (0, 0, 0, 0), 
                            width             = 3, 
                            height            = 3)
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

    #create the buttons in the Instruments tab (frame1)
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
                                      command   = self.toggleFan,  
                                      image     = self.ironImage,
                                      style     = "Normal.TButton")    
    self.solder_button.grid(          row       = 0, 
                                      column    = 2)
    self.io1_button       = Button(   frame1,           
                                      text      = "GPIO 1",            
                                      command   = self.bigRelay1,  
                                      image     = self.gpioONImage,
                                      style     = "Normal.TButton")    
    self.io1_button.grid(             row       = 1, 
                                      column    = 0)
    self.io2_button       = Button(   frame1,           
                                      text      = "GPIO 2",            
                                      command   = self.bigRelay2,  
                                      image     = self.gpioONImage,
                                      style     = "Normal.TButton")    
    self.io2_button.grid(             row       = 1, 
                                      column    = 1)
    self.io3_button       = Button(   frame1,           
                                      text      = "GPIO 3",            
                                      command   = self.relay1Toggle,  
                                      image     = self.gpioONImage,
                                      style     = "Normal.TButton")
    self.io3_button.grid(             row       = 1, 
                                      column    = 2)

    #Create the UI in the Camera tab (frame2)
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
                                          rowspan   = 2)

    intervalPhotoButton       = Button(   cameraFrameLeft,           
                                          text      = "Interval",          
                                          command   = self.startIntervalStill,  
                                          image     = self.intervalCamera,
                                          style     = "Normal.TButton")    

    intervalPhotoButton.grid(             row       = 2, 
                                          column    = 0,  
                                          rowspan   = 2)

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
    
    self.intervalText.grid(               row         = 1,
                                          column      = 2,
                                          columnspan  = 2,
                                          rowspan     = 2)

    increaseInterval.grid(                row         = 3,
                                          column      = 3)

    decreaseInterval.grid(                row         = 3,
                                          column      = 2)

    self.cameraStatus         = Label(    cameraFrameLeft, 
                                          text        = "NOT RECORDING", 
                                          style       = "cameraInfoLabel.TLabel")

    self.cameraStatus.grid(               row         = 4,
                                          column      = 2,
                                          columnspan  = 2)

    #Create the UI in the Environment tab (frame3)
    self.environmentTimeLabel         = Label(    frame3, 
                                          text        = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                                          style       = "EnrironmentTime.TLabel")
    
    self.environmentTimeLabel.grid(       row         = 5, 
                                          column      = 1,  
                                          columnspan  = 5)
    
    self.temperatureLabel            = Label(    frame3, 
                                          text        = "-", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityLabel               = Label(    frame3, 
                                          text        = "-", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityLabel.grid(              row         = 3, 
                                          column      = 1)

    self.temperatureLabel.grid(           row         = 2, 
                                          column      = 1)
    
    self.temperatureUnitLabel            = Label(    frame3, 
                                          text        = "\u00b0C", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityUnitLabel               = Label(    frame3, 
                                          text        = "%", 
                                          style       = "Enrironment.TLabel")
    
    self.humidityUnitLabel.grid(          row         = 3, 
                                          column      = 2)
    
    self.temperatureUnitLabel.grid(       row         = 2, 
                                          column      = 2)



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
      self.directory_interval       = '../photos/Interval_{}'.format(datetime.datetime.now().strftime("%B_%d_%y_%H_%M_%S"))  
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
      file_name               = '../videos/{}.h264'.format(datetime.datetime.now().strftime("%B_%d_%y_%H_%M_%S"))
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
    file_name = '../photos/{}.jpg'.format(datetime.datetime.now().strftime("%B_%d_%y_%H_%M_%S"))
    self.camera.capture(file_name)
    self.log_textBox.insert(0.0, "Captured image {}\n".format(file_name))

    image           = Image.open(file_name)
    image           = image.resize((360, 216), Image.ANTIALIAS) 
    self.last_photo = ImageTk.PhotoImage(image)
    Label(self.cameraFrameRight, image=self.last_photo).grid(row=0, column=0)
    
  def bigRelay1(self):
    self.pfr.x_pins[2].toggle()
    if self.pfr.x_pins[2].value == 0:
      relay_value = "ON"  
      self.io1_button.config(image=self.gpioONImage,style="Selected.TButton")
    else: 
      relay_value = "OFF"
      self.io1_button.config(image=self.gpioONImage,style="Normal.TButton")
    self.log_textBox.insert(0.0, "BigRelay1 is {}\n".format(relay_value))

  def bigRelay2(self):
    self.pfr.x_pins[3].toggle()
    if self.pfr.x_pins[3].value == 0:
      relay_value = "ON"  
      self.io2_button.config(image=self.gpioONImage,style="Selected.TButton")
    else: 
      relay_value = "OFF"
      self.io2_button.config(image=self.gpioONImage,style="Normal.TButton")
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


  def getDHTreadings(self):
    # Here is how to implement the sensor so that SUDO is not required
    # http://www.rototron.info/dht22-tutorial-for-raspberry-pi/
    # This works ok with Python 3
    DHT_SENSOR_TYPE   = 2302
    DHT_FREQUENCY     = 10000
    pi      = pigpio.pi()
    sensor  = DHT22.sensor(pi, 4)
    sensor.trigger()
    sleep(.2) # Necessary on faster Raspberry Pi's
    # To convert Celsius to Farenheit, use this formula: (°C × 9/5) + 32 = °F
    temperature = sensor.temperature()
    humidity    = sensor.humidity()
    sensor.cancel()
    pi.stop()
    self.temperatureLabel.config(     text  =  "{:3.2f}".format(temperature / 1.))
    self.humidityLabel.config(        text  =  "{:3.2f}".format(humidity / 1.))
    self.environmentTimeLabel.config( text  =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))           # Prints out to the terminal
    print("{:3.2f}, {:3.2f}".format(temperature / 1., humidity / 1.))   # Prints out to the terminal
    self.root.after(DHT_FREQUENCY, self.getDHTreadings)

  #With this method, I am testing interrupts from the GPIOs (i.e. to deal with a button press)
  # def print_flag(self,event):
  #   self.log_textBox.insert(0.0, "Light is {}\n".format(event.interrupt_flag))
      # print(event.interrupt_flag)

def main():
  root = Tk()
  root.attributes('-zoomed', True)
  ex = BenchComputer(root)
  root.after(DHT_FREQUENCY, ex.getDHTreadings)
  root.mainloop()  

if __name__ == '__main__':
    main()  
