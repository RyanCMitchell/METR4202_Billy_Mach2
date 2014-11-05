#!/usr/bin/env python
# @file NXTBrick.py
# -*- coding:shift_jis -*-

import nxt.locator
from nxt.sensor import *
from nxt.motor import *

class NXTBrick:
    def __init__(self, bsock=None):
        """
        Constructor
        Connect to a NXT brick, control motors and sensors, and reset odometry.
        """
        if bsock:
            self.sock = bsock
        else:
            self.sock = nxt.locator.find_one_brick().connect()

        self.motors = [Motor(self.sock, PORT_A),
                       Motor(self.sock, PORT_B),
                       Motor(self.sock, PORT_C)]
           
        self.sensors = [TouchSensor(self.sock, PORT_1),
                        SoundSensor(self.sock, PORT_2),
                        LightSensor(self.sock, PORT_3),
                        UltrasonicSensor(self.sock, PORT_4)]
        self.resetPosition()

    def close(self):
        """
        Close the connection to the NXT.
        """
        self.sock.close()

    def resetPosition(self, relative = 0):
        """
        Reset the NXT motor encoders.
        """
        for m in self.motors:
            m.reset_position(relative)

    def setMotors(self, vels):
        """
        Receive an array, set the motor power levels.
        If the length of vels is not equal to the number of motors,
        the smaller of the two values is used.
        """
        for i, v in enumerate(vels[:min(len(vels),len(self.motors))]):
            self.motors[i].power = max(min(v,127),-127)
            self.motors[i].mode = MODE_MOTOR_ON | MODE_REGULATED
            self.motors[i].regulation_mode = REGULATION_MOTOR_SYNC
            self.motors[i].run_state = RUN_STATE_RUNNING
            self.motors[i].tacho_limit = 0
            self.motors[i].set_output_state()

    def getMotors(self):
        """
        Read the motor encoder angles.
         
        """
        state = []
        for m in self.motors:
            state.append(m.get_output_state())
        return state

    def getSensors(self):
        """
        Read the sensor values, return them in an array.
        """
        state = []
        for s in self.sensors:
            state.append(s.get_sample())
        return state
 
 
"""
Test program
Set a suitable motor value, read their encoders.
Read sensor values and display them.
"""
if __name__ == "__main__":
    import time
    nxt = NXTBrick()
    print "connected"
    
    # Motor test
    for i in range(100):
        nxt.setMotors([80,-80,80])
        print "Motor: "
        mstat = nxt.getMotors()
        for i, m in enumerate(mstat):
            print "(" , i, "): ", m
        time.sleep(0.1)
    nxt.setMotors([0,0,0])
 
    # Sensor test
    for i in range(100):
        sensors = ["Touch", "Sound", "Light", "USonic"]
        sval = nxt.getSensors()
        for s in sensors:
            print s + ": " + sval
            print ""
            time.speel(0.1)
