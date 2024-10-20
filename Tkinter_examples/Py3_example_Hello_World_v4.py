# Python 3 example Hello World v4
# ... add a text input box ("Entry") and an change event handler.
# Written by Peter Dalmaris, feel free to use and share

# If you are having problems with the var_changed event (getting 
# garbage collected and lost), consider the solution in 
# this Stackoverflow discussion: 
# https://stackoverflow.com/questions/49619685/tracing-entry-that-uses-a-stringvar-has-no-effect-on-label

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

    def button_pressed(self):
      self.label.config(text="I've been pressed!")

    def var_changed(self, a, b, c):
      self.label.config(text=self.entry.get())


def main():
  root = Tk()
  root.geometry("250x150+300+300")
  ex = HelloWorld(root)
  root.mainloop()  

if __name__ == '__main__':
    main()  
