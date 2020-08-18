#import evdev
from evdev import InputDevice, categorize, ecodes
import ser as commands

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
print(gamepad.capabilities(verbose=True))

speed=500 # speed in mm/s
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

commands.writeABC()
commands.initialize()

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        print('---')
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
                commands.driveRadius(speed,-radius)
                print('Radius Test')
            if event.value==eventReleased: #312 is select button
                commands.driveStraight(0)
                RotationDirection=eOff
                StraightDirection=eOff
                print('Off')
        elif event.code==313 & event.value==eventPressed: #313 is start button
            commands.stop()
        else:
            if event.value==eventPressed:
                print(event.code)
    if event.type == ecodes.EV_ABS:
        print('---')
        if event.code==1: #1 is forwards/backwards
            RotationDirection=eOff
            if event.value==eDPAD_MIDDLE: #128 is middle position
                commands.driveStraight(0)
                StraightDirection=eOff
                print('Off')
            elif event.value==eDPAD_FORWARD: #0 is forwards position:
                commands.driveStraight(speed)
                StraightDirection=ePos
                print('Forward')
            elif event.value==eDPAD_BACKWARD: #255 is backwards position:
                commands.driveStraight(-speed)
                StraightDirection=eNeg
                print('Reverse')
        if event.code==0: #0 is left/right
            StraightDirection=eOff
            if event.value==eDPAD_MIDDLE: #128 is middle position
                commands.driveStraight(0)
                RotationDirection=eOff
                print('Off')
            elif event.value==eDPAD_LEFT: #0 is left position:
                commands.turnLeft(speed)
                RotationDirection=ePos
                print('Left')
            elif event.value==eDPAD_RIGHT: #255 is right position:
                commands.turnRight(speed)
                RotationDirection=eNeg
                print('Right')



