# Python 3 example Hello World v2

from tkinter import *

class HelloWorld:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="Hello"
            )
        self.button.pack(side=LEFT, padx=5)

        self.label = Label(frame, text="This is a label")
        self.label.pack()


def main():
  root = Tk()
  root.geometry("250x150+300+300")
  ex = HelloWorld(root)
  root.mainloop()  

if __name__ == '__main__':
    main()  