# Python 3 example Hello World
# A place to start with Python 3 and Tkinter
# Written by Peter Dalmaris, feel free to use and share

from tkinter import *

class HelloWorld:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="Hello"
            )
        self.button.pack()

def main():
  root = Tk()
  root.geometry("250x150+300+300")
  ex = HelloWorld(root)
  root.mainloop()  

if __name__ == '__main__':
    main()  