# -*- coding: utf-8 -*-
from os.path import isfile, join
from os import listdir
import numpy as np
import freenect, itertools, sys, time, cv2
import time
from matplotlib import pyplot as plt
from math import sqrt
from MatchingFunctions import findKeyPoints, drawKeyPoints, match, findKeyPointsDist, drawImageMappedPoints, saveImageMappedPoints, MatchAllCapture, Cluster, fit_ellipses
from CoordTransform import convertToWorldCoords, transformCoords, FrameFind
from MatchGlass import GlassFind

def MatchAllCluster(save, maxdist=200, filtparam=2.0, SplitTend = 0.8, glassDetect = 0, drawnoncups = 0):
    "This function attempts to find and classify cups on the turn table"

    #Acquire image
    img0, timestamp = freenect.sync_get_video()
    depth0, timestamp = freenect.sync_get_depth(format=freenect.DEPTH_REGISTERED)

    #Retieve the coordinate system
    Corners = np.load('CalibrationImages/Caliboutput/corners.npy')
    PixCorners = np.load('CalibrationImages/Caliboutput/PixCorners.npy')

    #Create ROI
    y0 = (PixCorners[1][0]+PixCorners[2][0])/2.
    x0 = (PixCorners[0][1]+PixCorners[2][2])/2.
    h = (PixCorners[2][0]-PixCorners[1][0])/2.
    w = (PixCorners[2][2]-PixCorners[0][1])/2.
    depth = depth0[y0-1.8*h:y0+1.7*h, x0-w*0.8:x0+w*0.5]
    img = img0[y0-1.8*h:y0+1.7*h, x0-w*0.8:x0+w*0.5]
    
    #Find all SIFT points relating to the cups
    PointsList, DisList, img, depth = MatchAllCapture(0,maxdist, img, depth)

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

    groups = distFromCenterAveList.index(min(distFromCenterAveList))+1
    segregated, centers, distFromCenter, distFromCenterAve = Cluster(Z, groups)


    #remove clusters that are <= 20 points or that are all superimposed
    i = 0
    while i < groups:
        if len(segregated[i]) <= 20 or np.isnan(np.std(segregated[i])):
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
                    
        #Find the edges of the middle of the cup using the voids
        #Attempt to find the centeral left edge
        try:
            del midLeft
        except NameError:
            pass
        i = 0
        Flag = True
        while Flag == True and i<cupDepth1.shape[0]:
            for k in xrange(cupDepth1.shape[1]/2,0,-1):
                if cupDepth2[cupDepth1.shape[0]-1-i,k] == 0:
                    midLeft = k+1
                    Flag = False
                    break
            i += 1
        #Catch non cups
        try:
            midLeft
        except NameError:
            continue
        leftDepth = cupDepth2[cupDepth1.shape[0]-1-i,midLeft]

        #Attempt to find the centeral right edge
        try:
            del midRight
        except NameError:
            pass
        i = 0
        Flag = True
        while Flag == True and i<cupDepth1.shape[0]:
            for k in xrange(cupDepth1.shape[1]/2,cupDepth1.shape[1]):
                if cupDepth2[cupDepth1.shape[0]-1-i,k] == 0:
                    midRight = k-1
                    Flag = False
                    break
            i += 1
            
        #Catch non cups
        try:
            midRight
        except NameError:
            continue
            
        rightDepth = cupDepth2[cupDepth1.shape[0]-1-i,midRight]

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
        globMin0 = int(round(centx-w+Minpos[0],0))
        globMin1 = int(round(centy-h+Minpos[1],0))
        globMax0 = int(round(centx-w+Maxpos[0],0))
        globMax1 = int(round(centy-h+Maxpos[1],0))
        globLeft = int(round(centx-w+midLeft,0))
        globRight = int(round(centx-w+midRight,0))
        CupMidTopPix = np.mean([[globMin0,globMin1],[globMax0,globMax1]],axis=0)
        CupMidTopPix = [int(CupMidTopPix[0]),int(CupMidTopPix[1])]
        CupMidTopPixList.append(CupMidTopPix)

        #Group the cup key points in lists
        FrontTopCup = [globMin0,globMin1,MinDepth]
        BackTopCup = [globMax0,globMax1,MaxDepth]
        LeftCup = [globLeft,centy,leftDepth]
        RightCup = [globRight,centy,rightDepth]

        #Find distances and midpoints between key points to help classify cups
        CupTopPoints = convertToWorldCoords([FrontTopCup,BackTopCup])
        CupTopWidth = np.linalg.norm(np.array(CupTopPoints[0])-np.array(CupTopPoints[1]))
        CupMidPoints = convertToWorldCoords([LeftCup,RightCup])
        CupMidWidth = np.linalg.norm(np.array(CupMidPoints[0])-np.array(CupMidPoints[1]))
        CupMidTop = [np.mean(CupTopPoints,axis=0)]
        CupMidTopWorld = transformCoords(CupMidTop, Corners)

        #Find a contour around the top of each cup
        blurThresh = cv2.blur(shape2,(5,5))
        #cv2.imshow('blur',blurThresh)
        thresh1 = 200
        thresh2 = 300
        edges = cv2.Canny(blurThresh,thresh1,thresh2)
        #cv2.imshow('edges',edges)
        contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)==0:
            continue
        cont = np.vstack(contours)
        hull = cv2.convexHull(cont)

        #Use the contour to determine fill    
        cupGray = cv2.cvtColor(cup1,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray',cupGray)
        ColourAverage = np.array([0,0,0])
        count = 0
        for i in xrange(Cutoff):
            for k in xrange(cupDepth1.shape[1]):
                if cv2.pointPolygonTest(hull,(k,i), False)>0:
                    ColourAverage += np.array(cupGray[i,k])
                    count += 1
        ColourAverageF = ColourAverage/count
        whiteColour = max(cupGray[Maxpos[1],Maxpos[0]], cupGray[Minpos[1],Minpos[0]])
        fillRatio = float(ColourAverageF[0])/whiteColour
        
        cv2.drawContours(cup1,[hull],0,colourList[j],2)
        #cv2.imshow('hull',cup1)

        #print "CupTopWidth",CupTopWidth,"CupMidWidth",CupMidWidth

        if CupMidWidth > CupTopWidth:
            
            cupOrientation = "Upsidedown"
            cupFill = "Empty"
            
            if CupTopWidth > 100:
                cupType = "Not a Cup"
            elif CupTopWidth > 58:
                cupType = "Large"
            elif CupTopWidth > 49:
                cupType = "Medium"
            elif CupTopWidth > 20:
                cupType = "Small"
            else:
                cupType = "Not a Cup"

        else:

            cupOrientation = "Upright"
            if fillRatio < 0.8:
                cupFill = "Full"
            else:
                cupFill = "Empty"
                
            if CupTopWidth > 100:
                cupType = "Not a Cup"
            elif CupTopWidth > 81:
                cupType = "Large"
            elif CupTopWidth > 69:
                cupType = "Medium"
            elif CupTopWidth > 30:
                cupType = "Small"
            else:
                cupType = "Not a Cup"

        
        #Draw the top of the bounding rectangle
        if cupType <> "Not a Cup":
            FinalCentersWC[j][0:3] = CupMidTopWorld[0]
            FinalCentersWC[j].append(cupType)
            FinalCentersWC[j].append(cupOrientation)
            FinalCentersWC[j].append(cupFill)

    FinalGlassCentersWC = []
    if glassDetect == 1:
        # Find the glass
        GlassCenters, GlassContours, GlassBox = GlassFind(img,depth)
        
        FinalGlassCenters = []
        FinalGlassCentersWC = []
        if len(GlassCenters)<>0:
            for i in xrange(1):
            #for i in xrange(len(GlassCenters)):
                box = GlassBox[i]
                cv2.drawContours(img,[GlassContours[i]],0,(255,255,255),2)
                cv2.rectangle(img,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),(255,255,255),2)
                glassx = box[0]+box[2]/2
                glassy = box[1] + box[3]
                cv2.circle(img, (glassx,glassy), 10, (255,255,255), -1)
                cv2.circle(img, (glassx,glassy), 2, (0,0,0), -1)

                z = 0
                runFlag = True
                glassDepth = 0
                while glassy+z<480 and runFlag == True:
                    if depth[glassy+z,glassx] <> 0:
                        glassDepth = depth[glassy+z,glassx]
                        runFlag = False
                    z += 1
                if glassDepth <> 0:
                    FinalGlassCenters.append([glassx,glassy,glassDepth])
                    
            if glassDepth <> 0:
                FinalGlassCentersCam = convertToWorldCoords(FinalGlassCenters)
                FinalGlassCentersWC = transformCoords(FinalGlassCentersCam, Corners)

                for i in xrange(1):
                #for i in xrange(len(GlassCenters)):
                    FinalGlassCentersWC[i][2] = FinalGlassCentersWC[i][2]+200
                    FinalGlassCentersWC[i] = ["Glass"]+FinalGlassCentersWC[i]
                    FinalGlassCentersWC[i].append("Empty")
                    cv2.putText(img,str(FinalGlassCentersWC[i]), (FinalGlassCenters[i][0]+20,FinalGlassCenters[i][1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0))
        
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
            cv2.circle(img, tuple(CupMidTopPixList[j]), 10, colourList[j], -1)
            cv2.circle(img, tuple(CupMidTopPixList[j]), 2, (0,0,0), -1)
            cv2.circle(img, centers[j], 2, (0,0,0), -1)
        else:
            deleteList.append(j)
            
    FinalFinalCentersWC = [i for j, i in enumerate(FinalCentersWC) if j not in deleteList]
    
    if save == 1:
        cv2.imwrite('ProcessedImages/ProcessedCluster'+str(ImageNo)+'.jpg', img)

    # Print or save final image
    if len(FinalGlassCentersWC)<>0:
        FinalFinalCentersWC.append(FinalGlassCentersWC)
    if len(FinalFinalCentersWC)<>0 or len(FinalGlassCentersWC)<>0:
        print FinalFinalCentersWC
        cv2.imshow("Cups Stream", img)


if __name__== '__main__':
    
    
    cv2.destroyAllWindows()

    #FrameFind()
    while 1<2:
        MatchAllCluster(0,maxdist=80, filtparam=2.0, SplitTend = 0.7, glassDetect = 0, drawnoncups = 1)
        cv2.waitKey(10)

    
    
        

    
