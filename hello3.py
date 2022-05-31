#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

# root window
root = tk.Tk()
root.title('Campus Register')
root.geometry("400x400")


class CampusRegistration:

    def __init__(self, master):
        myFrame = Frame(master)
        myFrame.pack()

        self.myButton = Button(master, text="Register", command=self.clicker)
        self.myButton.pack(pady=20)

    def clicker(self):
        myLabel = Label(root, text="Register with us!")
        myLabel.pack()


c = CampusRegistration(root)

root.mainloop()
