from tkinter import *


class MyTk:
    def __init__(self):
        self.Win = Tk()
        self.Win.title('Q&A platform for Python')
        screenwidth = self.Win.winfo_screenwidth()
        screenheight = self.Win.winfo_screenheight()
        width = 600
        height = 400
        alignStr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.Win.geometry(alignStr)
        self.Win.iconbitmap("D:\pyHomework/python2.ico")
        self.frame = Frame(self.Win)
        self.frame.place(relx=.5, rely=.5, anchor='center')
