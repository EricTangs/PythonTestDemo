from tkinter import *

def ProcessOk():
    print("Ok button is Clicked")

def processCancel():
    print("Cancel button is Clicked")

window=Tk()
btnOk = Button(window,text="Ok",fg="red",command=ProcessOk)
btnCancel=Button(window,text="Cancel",fg="yellow",command=processCancel)

btnOk.pack()
btnCancel.pack()

window.mainloop()
