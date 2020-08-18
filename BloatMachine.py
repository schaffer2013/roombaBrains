#import evdev
from evdev import InputDevice, categorize, ecodes
import ser as commands
import roombaCamera as camera

#creates object 'gamepad' to store the data
#you can call it whatever you like

gamepad = InputDevice('/dev/input/event1')
print('Trying 1... This device:' +gamepad.name)

if (gamepad.name!='PC Game Controller'):
    gamepad = InputDevice('/dev/input/event2')
    print('Trying 2... This device:' +gamepad.name)

if (gamepad.name!='PC Game Controller'):
    gamepad = InputDevice('/dev/input/event3')    
    print('Trying 3... This device:' +gamepad.name)



#prints out device info at start  
print(gamepad)
#print(gamepad.capabilities(verbose=True))

speed=200 # speed in mm/s
radius=250 # radius in mm

ePos=1
eNeg=-1
eOff=0
eDPAD_MIDDLE=128
eDPAD_FORWARD=0
eDPAD_BACKWARD=255
eDPAD_RIGHT=255
eDPAD_LEFT=0

RotationDirection=eOff
StraightDirection=eOff

radiusSelection=False
speedSelection=False

eventPressed=1
eventReleased=0

FirstEvent=True

##commands.writeABC()
##commands.initialize()

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if FirstEvent:
        commands.writeABC()
        commands.initialize()
        FirstEvent=False
    if event.type == ecodes.EV_KEY:
        if event.code==309: #309 is right bumper
            if event.value==eventPressed:
                speed+=100
                if speed>500:
                    speed=500
                print('Speed is: '+str(speed))
        elif event.code==308: #308 is left
            if event.value==eventPressed:
                speed-=100
                if speed<100:
                    speed=100
                print('Speed is: '+str(speed))
        elif event.code==312:
            if event.value==eventPressed: #312 is select button
                print('Select Button Down')
            if event.value==eventReleased: #312 is select button
                print('Select Button Up')
        elif event.code==313: #313 is start button
            if event.value==eventPressed:
                commands.stop()
        elif event.code==307:
            if event.value==eventPressed: #307 is Y button
                camera.viewAndSnap(10)
        elif event.code==304:
            if event.value==eventPressed: #304 is X button
                commands.clean()
        else:
            if event.value==eventPressed:
                print(event.code)
    if event.type == ecodes.EV_ABS: 
        if event.code==1: #1 is forwards/backwards
            if event.value==eDPAD_MIDDLE: #128 is middle position
                StraightDirection=eOff
                if RotationDirection==ePos:
                    commands.turnLeft(speed)
                elif RotationDirection==eNeg:
                    commands.turnRight(speed)
                else:
                    commands.driveStraight(0)
            elif event.value==eDPAD_FORWARD: #0 is forwards position:
                StraightDirection=ePos
                if RotationDirection==ePos:
                    commands.driveRadius(speed, radius)
                elif RotationDirection==eNeg:
                    commands.driveRadius(speed, -radius)
                else:
                    commands.driveStraight(speed)
            elif event.value==eDPAD_BACKWARD: #255 is backwards position:
                StraightDirection=eNeg
                if RotationDirection==ePos:
                    commands.driveRadius(-speed, radius)
                elif RotationDirection==eNeg:
                    commands.driveRadius(-speed, -radius)
                else:
                    commands.driveStraight(-speed)
        if event.code==0: #0 is left/right
            if event.value==eDPAD_MIDDLE: #128 is middle position
                RotationDirection=eOff
                if StraightDirection==ePos:
                    commands.driveStraight(speed)
                elif StraightDirection==eNeg:
                    commands.driveStraight(-speed)
                else:
                    commands.driveStraight(0)
            elif event.value==eDPAD_LEFT: #0 is left position:
                RotationDirection=ePos
                if StraightDirection==ePos:
                    commands.driveRadius(speed, radius)
                elif StraightDirection==eNeg:
                    commands.driveRadius(-speed, radius)
                else:
                    commands.turnLeft(speed)
                
            elif event.value==eDPAD_RIGHT: #255 is right position:
                RotationDirection=eNeg
                if StraightDirection==ePos:
                    commands.driveRadius(speed, -radius)
                elif StraightDirection==eNeg:
                    commands.driveRadius(-speed, -radius)
                else:
                    commands.turnRight(speed)
