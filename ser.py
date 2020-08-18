import serial, sys
import roombaTesting as api
import time
import threading
from time import sleep
from SensorFrame import SensorFrame

#test header for git

def initialize():
    if (ser.open):
        print('Connected')
        start()
        safeMode()
        ser.reset_input_buffer()
    else:
        print('Connection Failed')         

def makeLedGreen():
    writeSer([139,2,0,255])

def makeLedRed():
    writeSer([139,2,225,255])
    
def start():
    writeSer([128])
    getSensor(api.OI_MODE)
    #print ('Start')

def powerDown():
    writeSer([133])
    print ('Power')
    
def fullMode():
    writeSer([132])
    getSensor(api.OI_MODE)

def safeMode():
    writeSer([131])
    getSensor(api.OI_MODE)
    #print ('Safe')

def turnLeft(speed):
    radius=1 #1 is special case for CCW
    twoByteRad=serialize(radius,65536)
    twoByteSpeed=serialize(speed,500)
    writeSer([137,twoByteSpeed[0],twoByteSpeed[1],twoByteRad[0],twoByteRad[1]])

def turnRight(speed):
    radius=-1 #-1 is special case for CW
    twoByteRad=serialize(radius,65536)
    twoByteSpeed=serialize(speed,500)
    writeSer([137,twoByteSpeed[0],twoByteSpeed[1],twoByteRad[0],twoByteRad[1]])

def driveStraight(speed):
    radius=32768 #32768 is special case for CW (0x8000)
    twoByteRad=serialize(radius,65536)
    twoByteSpeed=serialize(speed,500)
    writeSer([137,twoByteSpeed[0],twoByteSpeed[1],twoByteRad[0],twoByteRad[1]])

def driveRadius(speed,radius):
    twoByteRad=serialize(radius,65536)
    twoByteSpeed=serialize(speed,500)
    writeSer([137,twoByteSpeed[0],twoByteSpeed[1],twoByteRad[0],twoByteRad[1]])

##def driveBack():
##    values=bytearray([137,255,205,127,0])
##    ser.write(values)

def stopMovement():
    safeMode() #check to see if in safe mode
    writeSer([146,0,0,0,0])

def shutdown():
    writeSer([173])
    getSensor(api.OI_MODE)

def forceDock():
    x=threading.Thread(target=passiveDocking)
    x.start()
    x.join()

def passiveDocking():
    flag=True
    charge=getSensor(api.BATTERY_CHARGE)
    sources=getSensor(api.CHARGING_SOURCES_AVAILABLE)
    if (sources==0):
        writeSer([143])
    while (flag):
        charge=getSensor(api.BATTERY_CHARGE)
        sources=getSensor(api.CHARGING_SOURCES_AVAILABLE)
        sleep(1)
        if (sources!=0):
            flag=False
    start()
    sys.exit()
        

def clean():
    writeSer([135])

def checkBump():
    writeSer([128,142,7])
    ch=read()
    return ord(ch)

def checkBattery():
    writeSer([128,142,25])
    ch=read()
    print(ch)
    if len(ch)==2:
        return _getTwoBytesUnsigned(ch[0],ch[1])    

    return False

def moveWhenNotCharging():
    deltaTime=60 #seconds
    lastCharge=0
    flag=True
    while (getSensor(api.CHARGING_STATE)==2 &flag):
        charge=getSensor(api.BATTERY_CHARGE)
        capacity=getSensor(api.BATTERY_CAPACITY)
        
        percentage=charge/capacity
        lastPercentage=lastCharge/capacity
        deltaPercentage=percentage-lastPercentage
        
        if (lastCharge!=0) & (deltaPercentage>0):
            secRemaining=math.floor(((1-percentage)/deltaPercentage)*deltaTime)
            minRemaining=secRemaining%60
            print("&s minutes and %s seconds remaining." % (minRemaining, secRemaining))
        if (lastCharge!=0) & (deltaPercentage==0):
            flag=False
        print (lastPercentage)
        print(deltaPercentage)

        lastCharge=charge
        sleep(deltaTime)
    goAndStop(-150)

def getBatteryContinuous():
    ser.reset_input_buffer()
    for i in range(100):
        charge=getSensor(api.BATTERY_CHARGE)
        print (charge)
        sleep(5)
    
def read(pauseTime=2):
    sleep(pauseTime)
    ch=ser.read_all()
    return ch

def reset():
    writeSer([7])

def goAndStop(speed=100,distance=250):
    mode=getSensor(api.OI_MODE)
    if (mode==api.SAFE_MODE or mode==api.FULL_MODE):
        driveStraight(speed)
        if speed!=0:
            sleep(abs(distance/speed))
        driveStraight(0)
        print(getSensor(api.DISTANCE))
    else:
        print("Wrong mode")

def writeABC():
    writeSer([164,78,67,68,69])

def writeSer(arg):
    values=bytearray(arg)
    ser.write(values)

def test():
    clean()
    sleep(2)
    stop()

def serialize(val,limit):
    if val > limit:
        val=limit
    if val < -limit:
        val=-limit
    modVal=val%65536
    highByte=int(modVal/256)
    #print (highByte)
    lowByte=modVal-highByte*256
    #print (lowByte)
    elements=[highByte,lowByte]
    twoByte=bytearray(elements)
    return twoByte    

def getSensor(packetID):
    if packetID>6:
        writeSer([142,int(packetID)])
        ch=ser.read(size=SENSOR_DATA_WIDTH[packetID])
        if len(ch)==1:
            val=sensorDataInterpreter[packetID](ch[0])
        elif len(ch)>1:
            val=sensorDataInterpreter[packetID](ch[0],ch[1])
        else:
            val=112233
        if packetID==api.OI_MODE:
            print(modeStr(val))
        else:
            print(val)
        return val
    elif packetID>-1:
        group=range(7,8) 
        if packetID==0:
            group=range(7,26+1)        
        if packetID==1:
            group=range(7,16+1)
        if packetID==2:
            group=range(17,20+1)         
        if packetID==3:
            group=range(21,26+1)
        if packetID==4:
            group=range(27,34+1)
        if packetID==5:
            group=range(35,42+1)
        if packetID==6:
            group=range(7,42+1)
        for i in group:
            getSensor(i)
def translate(cmd,val1=0,val2=0,val3=0):
    print(type(cmd))
    if cmd=='initialize':
        print ("We in it")
        initialize()
    elif cmd == 'makeLedGreen':
        makeLedGreen()
    elif cmd == 'makeLedRed':
        makeLedRed()
    elif cmd == 'start':
        start()
    elif cmd == 'fullMode':
        fullMode()
    elif cmd == 'turnLeft':
        turnLeft(int(val1))
    elif cmd == 'turnRight':
        turnRight(int(val1))
    elif cmd == 'driveStraight':
        driveStraight(int(val1))
    elif cmd == 'stop':
        stop()
    elif cmd == 'shutdown':
        shutdown()
    elif cmd == 'forceDock':
        forceDock()
    elif cmd == 'checkBump':
        checkBump()
    elif cmd == 'goAndStop':
        goAndStop()
    elif cmd == 'writeABC':
        writeABC()
    else:
        return 'Error'

def _getLower5Bits( r ):
    """ r is one byte as an integer """
    return [ _bitOfByte(4,r), _bitOfByte(3,r), _bitOfByte(2,r), _bitOfByte(1,r), _bitOfByte(0,r)]

def _getOneBit( r ):
    """ r is one byte as an integer """
    if r == 1:
        return 1
    else:
        return 0
    
def _getOneByteUnsigned( r ):
    """ r is one byte as an integer """
    return r
    
def _getOneByteSigned( r ):
    """ r is one byte as a signed integer """
    return _twosComplementInt1byte( r )
    
def _getTwoBytesSigned( r1, r2 ):
    """ r1, r2 are two bytes as a signed integer """
    return _twosComplementInt2bytes( r1, r2 )
    
def _getTwoBytesUnsigned( r1, r2 ):
    """ r1, r2 are two bytes as an unsigned integer """
    return r1 << 8 | r2
    
def _getButtonBits( r ):
    """ r is one byte as an integer """
    return [ _bitOfByte(2,r), _bitOfByte(0,r) ]

def getMode():
    ch=getSensor(35)
    return modeStr(int(ch[0]))
    

def modeStr( mode ):
    """ prints a string representing the input SCI mode """
    if mode == api.OFF_MODE: return 'OFF_MODE'
    if mode == api.PASSIVE_MODE: return 'PASSIVE_MODE'
    if mode == api.SAFE_MODE: return 'SAFE_MODE'
    if mode == api.FULL_MODE: return 'FULL_MODE'
    print('Warning: unknown mode', mode, 'seen in modeStr')
    return 'UNKNOWN_MODE'

#
# some module-level functions for dealing with bits and bytes
#
def _bytesOfR( r ):
    """ for looking at the raw bytes of a sensor reply, r """
    print('raw r is', r)
    for i in range(len(r)):
        print('byte', i, 'is', ord(r[i]))
    print('finished with formatR')

def _bitOfByte( bit, byte ):
    """ returns a 0 or 1: the value of the 'bit' of 'byte' """
    if bit < 0 or bit > 7:
        print('Your bit of', bit, 'is out of range (0-7)')
        print('returning 0')
        return 0
    return ((byte >> bit) & 0x01)

def _toBinary( val, numbits ):
    """ prints numbits digits of val in binary """
    if numbits == 0:  return
    _toBinary( val>>1 , numbits-1 )
    print((val & 0x01), end=' ')  # print least significant bit


def _fromBinary( s ):
    """ s is a string of 0's and 1's """
    if s == '': return 0
    lowbit = ord(s[-1]) - ord('0')
    return lowbit + 2*_fromBinary( s[:-1] )


def _twosComplementInt1byte( byte ):
    """ returns an int of the same value of the input
    int (a byte), but interpreted in two's
    complement
    the output range should be -128 to 127
    """
    # take everything except the top bit
    topbit = _bitOfByte( 7, byte )
    lowerbits = byte & 127
    if topbit == 1:
        return lowerbits - (1 << 7)
    else:
        return lowerbits


def _twosComplementInt2bytes( highByte, lowByte ):
    """ returns an int which has the same value
    as the twosComplement value stored in
    the two bytes passed in
    
    the output range should be -32768 to 32767
    
    chars or ints can be input, both will be
    truncated to 8 bits
    """
    # take everything except the top bit
    topbit = _bitOfByte( 7, highByte )
    lowerbits = highByte & 127
    unsignedInt = lowerbits << 8 | (lowByte & 0xFF)
    if topbit == 1:
        # with sufficient thought, I've convinced
        # myself of this... we'll see, I suppose.
        return unsignedInt - (1 << 15)
    else:
        return unsignedInt


def _toTwosComplement2Bytes( value ):
    """ returns two bytes (ints) in high, low order
    whose bits form the input value when interpreted in
    two's complement
    """
    # if positive or zero, it's OK
    if value >= 0:
        eqBitVal = value
    # if it's negative, I think it is this
    else:
        eqBitVal = (1<<16) + value
    
    return ( (eqBitVal >> 8) & 0xFF, eqBitVal & 0xFF )

sensorDataInterpreter = [ None, # 0
                          None, # 1
                          None, # 2
                          None, # 3
                          None, # 4
                          None, # 5
                          None, # 6
                          _getLower5Bits, # 7 BUMPS_AND_WHEEL_DROPS
                          _getOneBit, # 8 WALL_IR_SENSOR
                          _getOneBit, # 9 CLIFF_LEFT = 9
                          _getOneBit, # 10 CLIFF_FRONT_LEFT = 10
                          _getOneBit, # 11 CLIFF_FRONT_RIGHT = 11
                          _getOneBit, # 12 CLIFF_RIGHT = 12
                          _getOneBit, # 13 VIRTUAL_WALL
                          _getLower5Bits, # 14 LSD_AND_OVERCURRENTS
                          _getOneBit, # 15 DIRT_DETECTED
                          _getOneBit, # 16 unused
                          _getOneByteUnsigned, # 17 INFRARED_BYTE
                          _getButtonBits, # 18 BUTTONS
                          _getTwoBytesSigned, # 19 DISTANCE
                          _getTwoBytesSigned, # 20 ANGLE
                          _getOneByteUnsigned, # 21 CHARGING_STATE
                          _getTwoBytesUnsigned, # 22 VOLTAGE
                          _getTwoBytesSigned, # 23 CURRENT
                          _getOneByteSigned, # 24 BATTERY_TEMP
                          _getTwoBytesUnsigned, # 25 BATTERY_CHARGE
                          _getTwoBytesUnsigned, # 26 BATTERY_CAPACITY
                          _getTwoBytesUnsigned, # 27 WALL_SIGNAL
                          _getTwoBytesUnsigned, # 28 CLIFF_LEFT_SIGNAL
                          _getTwoBytesUnsigned, # 29 CLIFF_FRONT_LEFT_SIGNAL
                          _getTwoBytesUnsigned, # 30 CLIFF_FRONT_RIGHT_SIGNAL
                          _getTwoBytesUnsigned, # 31 CLIFF_RIGHT_SIGNAL
                          _getLower5Bits, # 32 CARGO_BAY_DIGITAL_INPUTS
                          _getTwoBytesUnsigned, # 33 CARGO_BAY_ANALOG_SIGNAL
                          _getOneByteUnsigned, # 34 CHARGING_SOURCES_AVAILABLE
                          _getOneByteUnsigned, # 35 OI_MODE
                          _getOneByteUnsigned, # 36 SONG_NUMBER
                          _getOneByteUnsigned, # 37 SONG_PLAYING
                          _getOneByteUnsigned, # 38 NUM_STREAM_PACKETS
                          _getTwoBytesSigned, # 39 REQUESTED_VELOCITY
                          _getTwoBytesSigned, # 40 REQUESTED_RADIUS
                          _getTwoBytesSigned, # 41 REQUESTED_RIGHT_VELOCITY
                          _getTwoBytesSigned, # 42 REQUESTED_LEFT_VELOCITY
                          _getTwoBytesUnsigned, # 43 Left Encoder Counts
                          _getTwoBytesUnsigned, # 44 Right Encoder Counts
                          _getOneByteUnsigned, # 45 LIGH_BUMP
                          _getTwoBytesUnsigned, # 46 LIGHTBUMP_LEFT
                          _getTwoBytesUnsigned, # 47 LIGHTBUMP_FRONT_LEFT
                          _getTwoBytesUnsigned, # 48 LIGHTBUMP_CENTER_LEFT
                          _getTwoBytesUnsigned, # 49 LIGHTBUMP_CENTER_RIGHT
                          _getTwoBytesUnsigned, # 50 LIGHTBUMP_FRONT_RIGHT
                          _getTwoBytesUnsigned, # 51 LIGHTBUMP_RIGHT                                  
                          None # only 51 as of right now
                          ]

SENSOR_DATA_WIDTH = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,2,2,1,2,2,2,2,2,2,2,1,2,1,1,1,1,1,2,2,2,2,2,2,1,2,2,2,2,2,2]


if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyUSB0",115200)
    ser.timeout=.1
    ser.reset_input_buffer()

    initialize()
    sf=SensorFrame()
    #print(sf.__str__())

    #x=threading.Thread(target=passiveDocking)
    #x.start()
