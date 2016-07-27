#!/usr/bin/python3

''' FILE NAME
bench_control.py
1. WHAT IT DOES
This is a GUI application that runs on any Raspberry Pi with a 40-pin header. 
It requires a Piface Realy Plus HAT

This version of the app implements the Instruments tab (Tab 1)
 
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
import  pifacerelayplus

PROGRAM_NAME      = "Tech Explorations Bench Controller"

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
    
    self.lightOnImage                           = PhotoImage(file="icons/light-bulb.png")    
    self.fanImage                               = PhotoImage(file="icons/ac.png")
    self.ironImage                              = PhotoImage(file="icons/iron-soldering.png")
    self.gpioONImage                            = PhotoImage(file="icons/switch.png")
    self.gpioOFFImage                           = PhotoImage(file="icons/switch-2.png")
    self.hairdryerImage                         = PhotoImage(file="icons/hairdryer.png")                                                        
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
    

    # Create the UI in the Environment tab (frame3)
    
    
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
  root.mainloop()  

if __name__ == '__main__':
    main()  
