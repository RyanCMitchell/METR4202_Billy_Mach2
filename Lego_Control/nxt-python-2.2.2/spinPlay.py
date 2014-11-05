#!/usr/bin/env python

import nxt.locator
from nxt.motor import *

def spin_around(LegoBrick):
    speed = 20
    rotation = 720
    MotorB = Motor(LegoBrick, PORT_B)
    MotorB.turn(speed, rotation)


LegoBrick = nxt.locator.find_one_brick()
spin_around(LegoBrick)

