# Python 2 example Hello World
# A place to start with Python 2 and Tkinter (we use Python 3 in the course)
# Written by Peter Dalmaris, feel free to use and share

from Tkinter import *

class HelloWorld:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="Hello", fg="red"
            )
        self.button.pack()

def main():
  root = Tk()  
  root.geometry("250x150+300+300")
  ex = HelloWorld(root)
  root.mainloop()  

if __name__ == '__main__':
    main() 