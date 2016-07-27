# Python 3 example Hello World v3

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

    def button_pressed(self):
      self.label.config(text="I've been pressed!")


def main():
  root = Tk()
  root.geometry("250x150+300+300")
  ex = HelloWorld(root)
  root.mainloop()  

if __name__ == '__main__':
    main()  