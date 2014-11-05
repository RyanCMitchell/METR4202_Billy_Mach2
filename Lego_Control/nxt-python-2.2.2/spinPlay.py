#!/usr/bin/env python

import nxt.locator
from nxt.motor import *

def spin_around(LegoBrick):
    speed = 20
    rotation = 720
    m_left = Motor(LegoBrick, PORT_B)
    m_left.turn(speed, rotation)


LegoBrick = nxt.locator.find_one_brick()
spin_around(LegoBrick)

