import picamera, os
import qrRead
from time import sleep

camera = picamera.PiCamera()

dirName='CameraImages'
imageName='image'

pathName=dirName+'/'+imageName+'.bmp'

def look(waitTime=3):
    camera.start_preview()
    sleep(waitTime)
    camera.stop_preview()

def takeImage():
    
    try:
        os.makedirs(dirName)    
        print("Directory " , dirName ,  " Created ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
    camera.capture(pathName,format='bmp')

def viewAndSnap(waitTime):
    look(waitTime)
    takeImage()

def decodeImage():
    print(qrRead.getString(pathName))


