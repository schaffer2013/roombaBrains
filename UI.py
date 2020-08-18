from tkinter import *
import serial
import time
import ser


def fullMode():
    ser.fullMode()

def stop():
    ser.stop()
    
class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.lightIsGreen=False
        self.button = Button(frame, 
                             text="DOCK", fg="red",
                             command=self.dock)
        self.button.pack(side=LEFT)
        self.slogan = Button(frame,
                             text="Stop",
                             command=stop)
        self.slogan.pack(side=LEFT)
    def write_slogan(self):
        if self.lightIsGreen:
            ser.makeLedRed()
        else:
            ser.makeLedGreen()
        self.lightIsGreen=~self.lightIsGreen
    def dock(self):
        ser.forceDock()

#ser = serial.Serial("COM4",115200)
#ser.timeout=.1
root = Tk()
root.title('Start Gui')
root.geometry('450x450')

app = App(root)
root.mainloop()
