# Python 3 example Hello World v7
# Shows how to use the Notebook widget
# Written by Peter Dalmaris, feel free to use and share

from tkinter import *
from tkinter.ttk import *

class HelloWorld:

    def __init__(self, master):
      frame = Frame(master)
      frame.pack()

      master.update()

      notebook  = Notebook(  frame, 
                          height  = master.winfo_height(),
                          width   = master.winfo_width())
                          
      frame1    = Frame() 
      frame2    = Frame() 
      frame3    = Frame()

      notebook.add(frame1,text  = "Instruments") 
      notebook.add(frame2,text  = "Camera") 
      notebook.add(frame3,text  = "Environment") 
      notebook.pack(pady = 5, side = LEFT)

      self.button = Button(
            frame1, text="Hello", command=self.button_pressed
            )
      self.button.pack(side=LEFT, padx=5)

      self.label = Label(frame2, text="This is a label")
      self.label.pack()

      a_var = StringVar()
      a_var.trace("w", self.var_changed)
      self.entry = Entry(frame2,textvariable=a_var)
      self.entry.pack()

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
      self.extractor_button = Button(   frame3,           
                                      text      = "Extractor",         
                                      command   = self.toggleFan,  
                                      image     = self.fanImage,
                                      style     = "Normal.TButton")
      self.extractor_button.pack()


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