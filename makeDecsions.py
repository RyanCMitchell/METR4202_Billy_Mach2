"Decision script"
import time
from math import sin,cos,sqrt, pi, atan2
import sys

sys.path.insert(0, "Vision/")
from BillyAll import *

cupInitPos = [[60,0,"Large"],[-60,0,"Medium"]]
t0 = time.time()
cupInitTime = [t0,t0]

def getCupPosition(ind,rpm):
    #Extract inital global variables
    [x0,y0,cupType] = cupInitPos[ind]
    t0 = cupInitTime[ind]
    theta0 = atan2(y0,x0)
    r = sqrt(x0**2+y0**2)
    t = time.time()-t0
    theta = rpm*(pi/30.)*t+theta0
    x_circle = r*cos(theta)
    y_circle = r*sin(theta)
    return x_circle,y_circle,cupType

def visualiseCup(ind,rpm):
    import cv2
    import numpy as np
    d_table = 255
    r_cupLarge = 45
    r_cupMedium = 39

    #initalise image
    img = np.zeros((300,300),dtype=np.uint8)
    si = img.shape
    cent = (si[0]/2,si[1]/2)
    cv2.circle(img, cent, d_table/2, [255,255,255])

    #raw cups
    for i in xrange(len(cupInitTime)):
        x,y,cupType = getCupPosition(i,rpm)
        if cupType == "Medium":
            r_cCup = r_cupMedium
        else:
            r_cCup = r_cupLarge
        c_cent = (cent[0]+int(round(x,0)),cent[1]+int(round(y,0)))
        cv2.circle(img, c_cent, r_cCup, [255,0,0])
        cv2.circle(img, c_cent, 1, [255,0,0])
    cv2.imshow('Cups',img)
    cv2.waitKey(1)
    
    

if __name__=='__main__':
    print MatchAllCluster(0,maxdist=60, filtparam=1.0, SplitTend = 0.7, ROI = 1, drawnoncups = 1)
    while True:
        visualiseCup(0,60/28.18)
    
    
