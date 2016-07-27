# Python 3 example Hello World v5

from tkinter import *

class HelloWorld:

    def __init__(self, master):
      frame = Frame(master)
      frame.pack()
      self.button = Button(
            frame, text="Hello", command=self.button_pressed
            )
      self.button.pack(side=LEFT, padx=5)

      self.label = Label(frame, text="This is a label")
      self.label.pack()

      a_var = StringVar()
      a_var.trace("w", self.var_changed)
      self.entry = Entry(frame,textvariable=a_var)
      self.entry.pack()

      self.fanImage = PhotoImage(file="icons/ac.png")
      self.extractor_button = Button(   frame,           
                                      text      = "Extractor",         
                                      command   = self.toggleFan,  
                                      image     = self.fanImage)
      self.extractor_button.pack()


    def button_pressed(self):
      self.label.config(text="I've been pressed!")

    def var_changed(self, a, b, c):
      self.label.config(text=self.entry.get())

    def toggleFan(self):
      self.label.config(text="Fan turned on")


def main():
  root = Tk()
  root.geometry("250x150+300+300")
  ex = HelloWorld(root)
  root.mainloop()  

if __name__ == '__main__':
    main()  