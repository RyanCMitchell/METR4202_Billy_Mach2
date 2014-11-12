import numpy as np
import freenect, itertools, sys, time, cv2
from MatchingFunctions import findKeyPoints, drawKeyPoints, match, findKeyPointsDist, drawImageMappedPoints, saveImageMappedPoints, MatchAllCapture, Cluster, fit_ellipses
from CoordTransform import convertToWorldCoords, transformCoords, FrameFind
from MatchGlass import GlassFind

#
img, timestamp = freenect.sync_get_video()
depth, timestamp = freenect.sync_get_depth(format=freenect.DEPTH_REGISTERED)

#Retieve the coordinate system
Corners = np.load('Vision/CalibrationImages/Caliboutput/corners.npy')
PixCorners = np.load('Vision/CalibrationImages/Caliboutput/PixCorners.npy')

#Draw the coordinate system
cv2.line(img, tuple(PixCorners[1][:2]), tuple(PixCorners[0][:2]), (255,0,0),3)
cv2.line(img, tuple(PixCorners[1][:2]), tuple(PixCorners[2][:2]), (0,0,255),3)

y0 = (PixCorners[1][0]+PixCorners[2][0])/2.
x0 = (PixCorners[0][1]+PixCorners[2][2])/2.
h = (PixCorners[2][0]-PixCorners[1][0])/2.
w = (PixCorners[2][2]-PixCorners[0][1])/2.

DepthROI = depth[y0-1.8*h:y0+1.7*h, x0-w*0.8:x0+w*0.5]
ImageROI = img[y0-1.8*h:y0+1.7*h, x0-w*0.8:x0+w*0.5]
cv2.imshow('img', ImageROI)
"""
#Choose pixel area likley to contain a cup
w = -0.08811*centdepth+103.0837
h = -0.13216*centdepth+154.6256
h = h*1.3
cup1 = depthimg[(centy-h):(centy), (centx-w):(centx+w)]
cup11 = np.copy(cup1)
cupDepth1 = depthmask[(centy-h):(FC[j][1]), (centx-w):(centx+w)]
cupDepth2 = np.copy(cupDepth1)


#Create blank binary images to fill with depth thresholds
shape1 = np.zeros(cupDepth1.shape,dtype=np.uint8)
shape2 = np.zeros(cupDepth1.shape,dtype=np.uint8)
shape3 = np.zeros(cupDepth1.shape,dtype=np.uint8)
"""
