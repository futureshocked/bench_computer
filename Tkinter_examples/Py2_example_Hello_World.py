# Python 2 example Hello World

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