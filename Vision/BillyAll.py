# -*- coding: utf-8 -*-
from os.path import isfile, join
from os import listdir
import numpy as np
import freenect, itertools, sys, time, cv2
import time
from matplotlib import pyplot as plt
from math import sin,cos,sqrt, pi, atan2
from MatchingFunctions import findKeyPoints, drawKeyPoints, match, findKeyPointsDist, drawImageMappedPoints, saveImageMappedPoints, MatchAllCapture, Cluster, fit_ellipses
from CoordTransform import convertToWorldCoords, transformCoords, FrameFind
from MatchGlass import GlassFind

cupInitPos = []
cupInitTime = []
t0 = time.time()

x_turnTableAxis = -181
y_turnTableAxis = 213

def MatchAllCluster(interationCount,save, maxdist=200, filtparam=2.0, SplitTend = 0.8, ROI = 0, glassDetect = 0, drawnoncups = 0):
    "This function attempts to find and classify cups on the turn table"

    #Acquire image
    img0, timestamp = freenect.sync_get_video()
    depth0, timestamp = freenect.sync_get_depth(format=freenect.DEPTH_REGISTERED)
    tCapture = time.time()
    
    #Retieve the coordinate system
    Corners = np.load('CalibrationImages/Caliboutput/corners.npy')
    PixCorners = np.load('CalibrationImages/Caliboutput/PixCorners.npy')

    #Create ROI
    y0 = (PixCorners[1][0]+PixCorners[2][0])/2.
    x0 = (PixCorners[0][1]+PixCorners[2][2])/2.
    h = (PixCorners[2][0]-PixCorners[1][0])/2.
    w = (PixCorners[2][2]-PixCorners[0][1])/2.
    ytop = y0
    xleft = x0-w
    depth = depth0[ytop:y0+4.*h, xleft:x0+w*0.3]
    img = img0[ytop:y0+4.*h, xleft:x0+w*0.3]
    
    #Find all SIFT points relating to the cups
    if ROI==1:
        PointsList, DisList, img, depth = MatchAllCapture(0,maxdist, img, depth)
    else:        
        PointsList, DisList, img, depth = MatchAllCapture(0,maxdist, img0, depth0)
        
    

    #Exclude SIFT points with no depth value
    PointsClusterList = []
    for i in xrange(len(PointsList)):
        if depth[PointsList[i].pt[1], PointsList[i].pt[0]] <> 0 and depth[PointsList[i].pt[1], PointsList[i].pt[0]] < 1000:
            PointsClusterList.append([PointsList[i].pt[0], PointsList[i].pt[1]])
    Z = np.array(PointsClusterList)

    #If there are not enough SIFT assume no cups present and show the unaltered image
    if len(Z) < 50:
        print "No Cups"
        cv2.imshow("Cups Stream", img)
        return
        
     
    # convert to np.float32
    Z = np.float32(Z)

    # Determine how many cups there are by trying clustering arrangements
    segregated, centers, distFromCenter, distFromCenterAve1 = Cluster(Z, 1)
    segregated, centers, distFromCenter, distFromCenterAve2 = Cluster(Z, 2)
    segregated, centers, distFromCenter, distFromCenterAve3 = Cluster(Z, 3)
    segregated, centers, distFromCenter, distFromCenterAve4 = Cluster(Z, 4)
    segregated, centers, distFromCenter, distFromCenterAve5 = Cluster(Z, 5)

    # Rank clustering arrangments and decide on the number of cups
    distFromCenterAveList = [(sum(distFromCenterAve1)/len(distFromCenterAve1))*1.0,
    (sum(distFromCenterAve2)/len(distFromCenterAve2))*(1.0+1.0*SplitTend),
    (sum(distFromCenterAve3)/len(distFromCenterAve3))*(1.0+2.0*SplitTend),
    (sum(distFromCenterAve4)/len(distFromCenterAve4))*(1.0+3.0*SplitTend),
    (sum(distFromCenterAve5)/len(distFromCenterAve5))*(1.0+4.0*SplitTend)]

    singleCup = 0

    if singleCup == 1:
        groups = 1
        segregated, centers, distFromCenter, distFromCenterAve = Cluster(Z, groups)
    else:
        groups = distFromCenterAveList.index(min(distFromCenterAveList))+1
        segregated, centers, distFromCenter, distFromCenterAve = Cluster(Z, groups)


    #remove clusters that are <= 300 points or that are all superimposed
    i = 0
    while i < groups:
        if len(segregated[i]) <= 300 or np.isnan(np.std(segregated[i])):
            del segregated[i], centers[i], distFromCenter[i], distFromCenterAve[i]
            groups -= 1
        i += 1

    #Create List for reduced points
    segregatedF = []
    for i in xrange(groups):
        segregatedF.append([])
        

    #Remove points which are not close to centroid
    for j in xrange(groups):
        for i in range(len(segregated[j])):
            if distFromCenter[j][i] < filtparam*distFromCenterAve[j]:
                segregatedF[j].append(segregated[j][i])

    for j in xrange(groups):
        segregatedF[j] = np.array(segregatedF[j])

    # Create a centriod depth list
    FinalCenters = []
    for j in xrange(groups):
        FinalCenters.append([centers[j][0], centers[j][1], depth[centers[j][1], centers[j][0]]])

    # Convert to world and then object coordinates
    FinalCentersCC = convertToWorldCoords(FinalCenters)
    Corners = np.load('CalibrationImages/Caliboutput/corners.npy')
    PixCorners = np.load('CalibrationImages/Caliboutput/PixCorners.npy')
    FinalCentersWC = transformCoords(FinalCentersCC, Corners)
    
    #Draw the coordinate system
    cv2.line(img, tuple(PixCorners[1][:2]), tuple(PixCorners[0][:2]), (255,0,0),3)
    cv2.line(img, tuple(PixCorners[1][:2]), tuple(PixCorners[2][:2]), (0,0,255),3)
    
    segregated = segregatedF
    FC = FinalCenters
    colourList=[(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]

    # Seperate the top of each cup in pixel space
    depthimg = img.copy()
    depthmask = depth.copy()

    CupMidTopPixList = []
    
    # Start Cup Classification loop
    for j in xrange(groups):
        centx = FC[j][0]
        centy = FC[j][1]
        centdepth = FC[j][2]
        
        # Choose pixel area likley to contain a cup
        w = -0.08811*centdepth+103.0837
        h = -0.13216*centdepth+154.6256
        h = h*1.3
        cup1 = depthimg[(centy-h):(centy), (centx-w):(centx+w)]
        cup11 = np.copy(cup1)
        cupDepth1 = depthmask[(centy-h):(FC[j][1]), (centx-w):(centx+w)]
        cupDepth2 = np.copy(cupDepth1)
        

        # Create blank binary images to fill with depth thresholds
        shape1 = np.zeros(cupDepth1.shape,dtype=np.uint8)
        shape2 = np.zeros(cupDepth1.shape,dtype=np.uint8)
        shape3 = np.zeros(cupDepth1.shape,dtype=np.uint8)
        
        #Show the voids within the ROI
        for i in xrange(cupDepth1.shape[0]):
            for k in xrange(cupDepth1.shape[1]):
                if cupDepth2[i,k] == 0:
                    shape3[i,k] = 255
        #cv2.imshow('depth',shape3)
                    

        # Fill with threshold depths
        upper = centdepth+100
        lower = centdepth-50
        depthRange = []
        depthRangePos = []
        for i in xrange(cupDepth1.shape[0]):
            for k in xrange(cupDepth1.shape[1]):
                if lower<cupDepth1[i,k]<upper:
                    shape1[i,k] = cupDepth1[i,k]
                    depthRange.append(cupDepth1[i,k])
                    depthRangePos.append([k,i])

        # Find the closest point within the ROI (the front top edge of the cup)
        if len(depthRange)==0:
            break
        MinDepth = min(depthRange)
        Minpos = depthRangePos[depthRange.index(min(depthRange))]
        Cutoff = Minpos[1]

        for i in xrange(Cutoff):
            for k in xrange(cupDepth1.shape[1]):
                if lower<cupDepth1[i,k]<upper:
                    shape2[i,k] = 255
        #cv2.imshow('thresh',shape2)

        # Find the front far edge of the cup
        q = 0
        runFlag = True
        while runFlag is True and q < Cutoff:
            for p in xrange(cupDepth1.shape[1]):
                if shape2[q,p] == 255:
                    Maxpos = [p,q]
                    MaxDepth = cupDepth1[q,p]
                    runFlag = False
                    break
            q += 1
        try:
            Maxpos
        except NameError:
            continue

        #Find the key points on the cup in world coordinates
        globMin0 = int(round(centx-w+xleft+Minpos[0],0))
        globMin1 = int(round(centy-h+ytop+Minpos[1],0))
        globMax0 = int(round(centx-w++xleft+Maxpos[0],0))
        globMax1 = int(round(centy-h+ytop+Maxpos[1],0))
        CupMidTopPix = np.mean([[globMin0,globMin1],[globMax0,globMax1]],axis=0)
        CupMidTopPix = [int(CupMidTopPix[0]),int(CupMidTopPix[1])]
        CupMidTopPixList.append(CupMidTopPix)

        #Group the cup key points in lists
        FrontTopCup = [globMin0,globMin1,MinDepth]
        BackTopCup = [globMax0,globMax1,MaxDepth]

        #Find distances and midpoints between key points to help classify cups
        CupTopPoints = convertToWorldCoords([FrontTopCup,BackTopCup])
        CupTopWidth = np.linalg.norm(np.array(CupTopPoints[0])-np.array(CupTopPoints[1]))
        CupMidTop = [np.mean(CupTopPoints,axis=0)]
        CupMidTopWorld = transformCoords(CupMidTop, Corners)


        #print "CupTopWidth",CupTopWidth
        if CupTopWidth > 100:
            cupType = "Not a Cup"
        elif CupTopWidth > 81:
            cupType = "Large"
        elif CupTopWidth > 50:
            cupType = "Medium"
        else:
            cupType = "Not a Cup"

        FinalCentersWC[j][0:3] = CupMidTopWorld[0]
        FinalCentersWC[j].append(cupType)

    # Draw the groups
    deleteList = []
    for j in xrange(groups):
        if len(FinalCentersWC[j]) > 3 or drawnoncups == 1:
            centerst = tuple(np.array(centers[j])+np.array([0,50]))
            cv2.putText(img,str(FinalCentersWC[j]), centerst, cv2.FONT_HERSHEY_SIMPLEX, 0.3, colourList[j])
            for i in range(len(segregated[j])):
                pt_a = (int(segregated[j][i,0]), int(segregated[j][i,1]))
                cv2.circle(img, pt_a, 3, colourList[j])
                cv2.line(img, pt_a, centers[j], colourList[j])
            if j>=len(CupMidTopPixList):
                continue
            topPixel = [int(CupMidTopPixList[j][0]-ytop),int(CupMidTopPixList[j][1]-xleft)]
            cv2.circle(img, tuple(topPixel), 10, colourList[j], -1)
            cv2.circle(img, tuple(topPixel), 2, (0,0,0), -1)
            cv2.circle(img, centers[j], 2, (0,0,0), -1)
        else:
            deleteList.append(j)
            
    FinalFinalCentersWC = [i for j, i in enumerate(FinalCentersWC) if j not in deleteList]
    
    if save == 1:
        cv2.imwrite('ProcessedImages/ProcessedCluster'+str(ImageNo)+'.jpg', img)

    # Print or save final image
    if len(FinalFinalCentersWC)<>0 or len(FinalGlassCentersWC)<>0:
        print FinalFinalCentersWC
        cv2.imshow("Cups Stream", img)

    
    # If kinect has run for a few iteration and there are less
    #than 5 cups accounted for start global decisions
    if interationCount>4 and len(cupInitPos)<=150:

        #print "FinalFinalCentersWC",FinalFinalCentersWC
        # remove all cups which couldn't be classified
        cupContenderList = []
        for i in FinalFinalCentersWC:
            if len(i)==4:
                if i[3]<>"Not a Cup":
                    cupContenderList.append(i)
                    
        #print "cupContenderList",cupContenderList
        # Remove all cups which aren't on the table
        cupContenderList1 = []
        for i in cupContenderList:
            if 50<i[2]<110:
                cupContenderList1.append(i)

        #print "cupContenderList1",cupContenderList1
        # Check if the model already has a cup there
        if len(cupContenderList1) > 0:
            global cupInitPos,cupInitTime
            cupInitPos.append(FinalFinalCentersWC[0])
            cupInitTime.append(tCapture-t0)
    

def getCupPosition(ind,rpm):
    #Extract inital global variables
    [x0,y0,z0,cupType] = cupInitPos[ind]
    x0 = x0 - x_turnTableAxis
    y0 = y0 - y_turnTableAxis
    t0cup = cupInitTime[ind]
    theta0 = atan2(x0,y0)
    r = sqrt(x0**2+y0**2)
    t = time.time()-t0-t0cup
    theta = rpm*(pi/30.)*t+theta0
    x_circle = r*sin(theta) + x_turnTableAxis
    y_circle = r*cos(theta) + y_turnTableAxis
    return x_circle,y_circle,cupType

def visualiseCup(rpm):
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
        x = x - x_turnTableAxis
        y = y - y_turnTableAxis
        
        if cupType == "Medium":
            r_cCup = r_cupMedium
        else:
            r_cCup = r_cupLarge
        c_cent = (cent[0]+int(round(y,0)),cent[1]+int(round(x,0)))
        cv2.circle(img, c_cent, r_cCup, [255,0,0])
        cv2.circle(img, c_cent, 1, [255,0,0])
        cv2.circle(img, (20,10), 1, [255,0,0])
    cv2.imshow('Cups',img)

if __name__== '__main__':
    
    
    cv2.destroyAllWindows()

    #FrameFind()
    interationCount = 0
    while 1<2:
        MatchAllCluster(interationCount,0,maxdist=60, filtparam=1.0, SplitTend = 0.7, ROI = 1, drawnoncups = 1)
        visualiseCup(60/30.88)
        cv2.waitKey(10)
        interationCount += 1
        

    
    
        

    
