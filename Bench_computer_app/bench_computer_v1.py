#!/usr/bin/python3

''' FILE NAME
bench_control.py
1. WHAT IT DOES
This is a GUI application that runs on any Raspberry Pi with a 40-pin header. 
It requires a Piface Realy Plus HAT

This version of the app implements the bare application with only the Notebook and text box (log) widgets.
 
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

PROGRAM_NAME      = "Tech Explorations Bench Controller"

class BenchComputer(Frame):

  def __init__(self, root):
    Frame.__init__(self, root)   

    root.protocol("WM_DELETE_WINDOW", self.on_closing)  # This will create a pop-up to confirm ending the program, and
                                                        # if there is confirmation it will call the on_closing method
                                                        # to tidy up before closing.
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
                          width   = self.root.winfo_width()-150)
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
    
    # Create the UI in the Control tab (frame1)
    

    # Create the UI in the Camera tab (frame2)
    

    # Create the UI in the Environment tab (frame3)
    
    

  def on_closing(self):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.root.destroy()

def main():
  root = Tk()
  root.attributes('-zoomed', True)
  ex = BenchComputer(root)
  root.mainloop()  

if __name__ == '__main__':
    main()  
