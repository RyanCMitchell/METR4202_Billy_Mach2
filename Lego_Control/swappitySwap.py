# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 10:59:50 2014

@author: Alistair
"""

def swappitySwap(degx,degy,degz):
    time = 1
    if abs(degx) < 52.5:
        if degx < 0:
            speed1 = -25
        else:
            speed1 = 25
    elif abs(degx) > 99:
        if degx < 0:
            speed1 = -99
        else:
            speed1 = 99
    else:
        speed1 = int(degx/time)
        
    if abs(degy) < 52.5:
        if degy < 0:
            speed2 = -25
        else:
            speed2 = 25
    elif abs(degy) > 99:
        if degy < 0:
            speed2 = -99
        else:
            speed2 = 99
    else:
        speed2 = int(degy/time)
        
    if abs(degz) < 52.5:
        if degz < 0:
            speed3 = -25
        else:
            speed3 = 25
    elif abs(degz) > 99:
        if degz < 0:
            speed3 = -99
        else:
            speed3 = 99
    else:
        speed3 = int(degz/time)

    x = abs(degx)
    y = abs(degy)
    z = abs(degz)        
        
    return [x,y,z,speed1,speed2,speed3]