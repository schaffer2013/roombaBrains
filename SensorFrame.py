import math

class SensorFrame:
    """ the sensorFrame class is really a struct whose
    fields are filled in by sensorStatus
    """
    
    def __init__(self):
        """ constructor -- set all fields to 0
        """
        self.casterDrop = 0
        self.leftWheelDrop = 0
        self.rightWheelDrop = 0
        self.leftBump = 0
        self.rightBump = 0
        self.wallSensor = 0
        self.leftCliff = 0
        self.frontLeftCliff = 0
        self.frontRightCliff = 0
        self.rightCliff = 0
        self.virtualWall = 0
        self.driveLeft = 0
        self.driveRight = 0
        self.mainBrush = 0
        self.vacuum = 0
        self.sideBrush = 0
        self.leftDirt = 0
        self.rightDirt = 0
        self.remoteControlCommand = 0
        self.powerButton = 0
        self.spotButton = 0
        self.cleanButton = 0
        self.maxButton = 0
        self.distance = 0
        self.rawAngle = 0
        self.angleInRadians = 0
        self.chargingState = 0
        self.voltage = 0
        self.current = 0
        self.temperature = 0
        self.charge = 0
        self.capacity = 0
        self.lightBumpLeft = 0
        self.lightBumpFrontLeft = 0
        self.lightCenterLeft = 0
        self.lightCenterRight = 0
        self.lightBumpFrontRight = 0
        self.lightBumpRight = 0
        self.dirt = 0
    
    def __str__(self):
        """ returns a string with the information
        from this SensorFrame
        """
        # there's probably a more efficient way to do this...
        # perhaps just making it all + instead of the separate
        # += would be more efficient
        #
        # actually, we should make a list and call ''.join(list)
        # not that we will...
        #
        s = ''
        s += 'casterDrop: ' + str(self.casterDrop) + '\n'
        s += 'leftWheelDrop: ' + str(self.leftWheelDrop) + '\n'
        s += 'rightWheelDrop: ' + str(self.rightWheelDrop) + '\n'
        s += 'leftBump: ' + str(self.leftBump) + '\n'
        s += 'rightBump: ' + str(self.rightBump) + '\n'
        s += 'wallSensor: ' + str(self.wallSensor) + '\n'
        s += 'leftCliff: ' + str(self.leftCliff) + '\n'
        s += 'frontLeftCliff: ' + str(self.frontLeftCliff) + '\n'
        s += 'frontRightCliff: ' + str(self.frontRightCliff) + '\n'
        s += 'rightCliff: ' + str(self.rightCliff) + '\n'
        s += 'virtualWall: ' + str(self.virtualWall) + '\n'
        s += 'driveLeft: ' + str(self.driveLeft) + '\n'
        s += 'driveRight: ' + str(self.driveRight) + '\n'
        s += 'mainBrush: ' + str(self.mainBrush) + '\n'
        s += 'vacuum: ' + str(self.vacuum) + '\n'
        s += 'sideBrush: ' + str(self.sideBrush) + '\n'
        s += 'leftDirt: ' + str(self.leftDirt) + '\n'
        s += 'rightDirt: ' + str(self.rightDirt) + '\n'
        s += 'remoteControlCommand: ' + str(self.remoteControlCommand) + '\n'
        s += 'powerButton: ' + str(self.powerButton) + '\n'
        s += 'spotButton: ' + str(self.spotButton) + '\n'
        s += 'cleanButton: ' + str(self.cleanButton) + '\n'
        s += 'maxButton: ' + str(self.maxButton) + '\n'
        s += 'distance: ' + str(self.distance) + '\n'
        s += 'rawAngle: ' + str(self.rawAngle) + '\n'
        s += 'angleInRadians: ' + str(self.angleInRadians) + '\n'
        # no data member needed for this next line
        s += 'angleInDegrees: ' + str(math.degrees(self.angleInRadians)) + '\n'
        s += 'chargingState: ' + str(self.chargingState) + '\n'
        s += 'voltage: ' + str(self.voltage) + '\n'
        s += 'current: ' + str(self.current) + '\n'
        s += 'temperature: ' + str(self.temperature) + '\n'
        s += 'charge: ' + str(self.charge) + '\n'
        s += 'capacity: ' + str(self.capacity) + '\n'
        return s
    
    def _toBinaryString(self):
        """ this converts the calling SensorFrame into a 26-byte
        string of the format the roomba sends back
        """
        # todo: handle the different subsets (frames) of sensor data
        
        # here are the 26 bytes in list form
        slist = [0]*26
        
        # First Frame
        
        # byte 0: bumps and wheeldrops
        slist[0] = self.casterDrop << 4 | \
            self.leftWheelDrop << 3 | \
            self.rightWheelDrop << 2 | \
            self.leftBump << 1 | \
            self.rightBump
        
        # byte 1: wall data
        slist[1] = self.wallSensor
        
        # byte 2: cliff left
        slist[2] = self.leftCliff
        # byte 3: cliff front left
        slist[3] = self.frontLeftCliff
        # byte 4: cliff front right
        slist[4] = self.frontRightCliff
        # byte 5: cliff right
        slist[5] = self.rightCliff
        
        # byte 6: virtual wall
        slist[6] = self.virtualWall
        
        # byte 7: motor overcurrents
        slist[7] = self.driveLeft << 4 | \
            self.driveRight << 3 | \
            self.mainBrush << 2 | \
            self.vacuum << 1 | \
            self.sideBrush
        
        # byte 8: dirt detector left
        slist[8] = self.leftDirt
        # byte 9: dirt detector left
        slist[9] = self.rightDirt
        
        # Second Frame
        
        # byte 10: remote control command
        slist[10] = self.remoteControlCommand
        
        # byte 11: buttons
        slist[11] = self.powerButton << 3 | \
            self.spotButton << 2 | \
            self.cleanButton << 1 | \
            self.maxButton
        
        # bytes 12, 13: distance
        highVal, lowVal = _toTwosComplement2Bytes( self.distance )
        slist[12] = highVal
        slist[13] = lowVal
        
        # bytes 14, 15: angle
        highVal, lowVal = _toTwosComplement2Bytes( self.rawAngle )
        slist[14] = highVal
        slist[15] = lowVal
        
        # Third Frame
        
        # byte 16: charging state
        slist[16] = self.chargingState
        
        # bytes 17, 18: voltage
        slist[17] = (self.voltage >> 8) & 0xFF
        slist[18] = self.voltage & 0xFF
        
        # bytes 19, 20: current
        highVal, lowVal = _toTwosComplement2Bytes( self.current )
        slist[19] = highVal
        slist[20] = lowVal
        
        # byte 21: temperature
        slist[21] = self.temperature
        
        # bytes 22, 23: charge
        slist[22] = (self.charge >> 8) & 0xFF
        slist[23] = self.charge & 0xFF
        
        # bytes 24, 25: capacity
        slist[24] = (self.capacity >> 8) & 0xFF
        slist[25] = self.capacity & 0xFF
        
        # convert to a string
        s = ''.join([ chr(x) for x in slist ])
        
        return s
