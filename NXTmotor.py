#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from time import sleep

def spin_around(b):
    m_left = Motor(b, PORT_B)
    m_right = Motor(b, PORT_A)
    m_left.turn(100, 50)
    m_right.turn(100, 50)

        
b = nxt.locator.find_one_brick()
spin_around(b)

