import tkinter
from tkinter import *


class InitialInterface:
    def __init__(self):
        self.initialWin = tkinter.Tk()
        self.initialWin.title('Q&A platform for Python')
        frame = Frame(self.initialWin)
        frame.pack()
        self.createInitial(frame)
        self.initialWin.mainloop()

    def createInitial(self, frame):
        loginButton = Button(frame, text='Login', command=self.createLogin)
        loginButton.pack()
        topQuitButton = Button(frame, text='topQuit', command=frame.quit)
        topQuitButton.pack()

    def createLogin(self):
        print("login")

initialInterface = InitialInterface()
