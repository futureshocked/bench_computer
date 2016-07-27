# Python 3 example Hello World v8
# This example demonstrates a basic use of the Grip layout manager
# Written by Peter Dalmaris, feel free to use and share

from tkinter import *
from tkinter.ttk import *

class HelloWorld:

    def __init__(self, master):
      frame = Frame(master)
      frame.pack()

      frame.columnconfigure(     0, pad    = 2)
      frame.columnconfigure(     1, pad    = 2)
      frame.rowconfigure(        0, pad    = 2) 
      frame.rowconfigure(        1, pad    = 2) 
      frame.rowconfigure(        2, pad    = 2) 


      self.button = Button(
            frame, text="Hello", command=self.button_pressed
            )
      #self.button.pack(side=LEFT, padx=5)
      self.button.grid(row=0, column=0, pady=10, padx=10, sticky=W+E+N+S)

      self.label = Label(frame, text="This is a label")
      #self.label.pack()
      self.label.grid(row=0, column=1)
      
      a_var = StringVar()
      a_var.trace("w", self.var_changed)
      self.entry = Entry(frame,textvariable=a_var)
      #self.entry.pack()
      self.entry.grid(row=1, column=0)

      buttonStyle = Style()
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

      self.fanImage = PhotoImage(file="icons/ac.png")
      self.addImage = PhotoImage(file="icons/add.png")
      self.extractor_button = Button(   frame,           
                                      text      = "Extractor",         
                                      command   = self.toggleFan,  
                                      image     = self.fanImage,
                                      style     = "Normal.TButton")
      #self.extractor_button.pack()
      self.extractor_button.grid(row=1, column=1)

      self.label2 = Label(frame, text="This is another label")
      self.label2.grid(row=2, column=0, columnspan  = 2)



    def button_pressed(self):
      self.label.config(text="I've been pressed!")

    def var_changed(self, a, b, c):
      self.label.config(text=self.entry.get())

    def toggleFan(self):
      self.label.config(text="Fan turned on")
      self.extractor_button.config(image=self.addImage,style="Selected.TButton")


def main():
  root = Tk()
  root.geometry("250x150+300+300")
  ex = HelloWorld(root)
  root.mainloop()  

if __name__ == '__main__':
    main()  