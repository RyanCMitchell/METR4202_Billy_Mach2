# -*- coding: utf-8 -*-
from os.path import isfile, join
from os import listdir
import numpy as np
import freenect, cv2
import thread
import time, sys, itertools
from matplotlib import pyplot as plt
from math import sin,cos,sqrt, pi, atan2, radians
#from MatchingFunctions import *
#from CoordTransform import convertToWorldCoords, transformCoords, FrameFind
from Vision.MatchingFunctions import *
from Vision.CoordTransform import convertToWorldCoords, transformCoords, FrameFind
from Lego_Control.runNxt import *
import Sound
#from MatchGlass import GlassFind

cupInitPos = []
cupInitTime = []
t0 = time.time()
cupAveInitPos = []
cupAveTime = 0.
cupCompletedPos = []

x_turnTableAxis = -176
y_turnTableAxis = 235
queueLength = 50

def MatchAllCluster(interationCount,save, tkpTdList, maxdist=200, filtparam=2.0, SplitTend = 0.8, ROI = 0, drawnoncups = 0):
    "This function attempts to find and classify cups on the turn table"

    #Acquire image
    img0, timestamp = freenect.sync_get_video()
    depth0, timestamp = freenect.sync_get_depth(format=freenect.DEPTH_REGISTERED)
    tCapture = time.time()
    
    #Retieve the coordinate system
    Corners = np.load('Vision/CalibrationImages/Caliboutput/corners.npy')
    PixCorners = np.load('Vision/CalibrationImages/Caliboutput/PixCorners.npy')

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
        PointsList, DisList, img, depth = MatchAllCapture(0,tkpTdList,maxdist, img, depth)
    else:        
        PointsList, DisList, img, depth = MatchAllCapture(0,tkpTdList,maxdist, img0, depth0)
        
    

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
    Corners = np.load('Vision/CalibrationImages/Caliboutput/corners.npy')
    PixCorners = np.load('Vision/CalibrationImages/Caliboutput/PixCorners.npy')
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
        cv2.imwrite('Vision/ProcessedImages/ProcessedCluster'+str(ImageNo)+'.jpg', img)

    # Print or save final image
    if len(FinalFinalCentersWC)<>0:# or len(FinalGlassCentersWC)<>0:
        #print FinalFinalCentersWC
        cv2.imshow("Cups Stream", img)

        
    # If kinect has run for a few iteration and there are less
    #than 5 cups accounted for start global decisions
    if interationCount>4:

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
            xtable = i[0] - x_turnTableAxis
            ytable = i[1] - y_turnTableAxis
            rthing = sqrt(xtable**2 + ytable**2)
            if (50<i[2]<110)and(rthing < 115.):
                cupContenderList1.append(i)

        #print "cupContenderList1",cupContenderList1
        # Check if the model already has a cup there
        for i in xrange(len(cupContenderList1)):
            global cupInitPos,cupInitTime
            cupInitPos.append(cupContenderList1[i])
            cupInitTime.append(tCapture-t0)
            if len(cupInitPos) > queueLength:
                del cupInitPos[0]
                del cupInitTime[0]

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

def getCupPositionAve(ind,rpm,tAhead):
    #Extract inital global variables
    [x0,y0,z0,cupType] = cupAveInitPos[ind]
    x0 = x0 - x_turnTableAxis
    y0 = y0 - y_turnTableAxis
    theta0 = atan2(x0,y0)
    r = sqrt(x0**2+y0**2)
    t = time.time()-t0-cupAveTime
    cupAveTimeTemp = cupAveTime
    theta = rpm*(pi/30.)*(t+tAhead)+theta0
    x_circle = r*sin(theta) + x_turnTableAxis
    y_circle = r*cos(theta) + y_turnTableAxis
    return x_circle,y_circle,cupType,x0,y0,cupAveTimeTemp

def visualiseCupAve(rpm,tAhead=5):
    d_table = 255
    r_cupLarge = 45
    r_cupMedium = 39

    #initalise image
    img = np.zeros((300,300,3),dtype=np.uint8)
    si = img.shape
    cent = (si[0]/2,si[1]/2)
    cv2.circle(img, cent, d_table/2, [255,255,255])

    #raw cups
    for i in xrange(len(cupAveInitPos)):
        x,y,cupType,x0,y0,cupAveTimeTemp = getCupPositionAve(i,rpm,0)
        

        x = x - x_turnTableAxis
        y = y - y_turnTableAxis
        
        if cupType == "Medium":
            r_cCup = r_cupMedium
            color = [255,0,0]
        else:
            r_cCup = r_cupLarge
            color = [0,255,0]
        c_cent = (cent[0]+int(round(y,0)),cent[1]+int(round(x,0)))
        cv2.circle(img, c_cent, 10, color, -1)
        cv2.circle(img, c_cent, r_cCup, color,thickness=5)
        cv2.circle(img, c_cent, 2, (0,0,0), -1)

    for i in xrange(len(cupCompletedPos)):
        temp = cupCompletedPos[i]
        [x0,y0,rpm,delayTime,cupAveTimeTemp] = temp
        x0,y0 = getCupPositionAtTime(x0,y0,rpm,delayTime,cupAveTimeTemp)
        x = x0 - x_turnTableAxis
        y = y0 - y_turnTableAxis
        color = [0,0,255]
        c_cent = (cent[0]+int(round(y,0)),cent[1]+int(round(x,0)))
        cv2.circle(img, c_cent, 10, color, -1)
        cv2.circle(img, c_cent, r_cupLarge, color,thickness=5)
        cv2.circle(img, c_cent, 2, (0,0,0), -1)
        
        

    """
    #ahead cups
    for i in xrange(len(cupAveInitPos)):
        x,y,cupType = getCupPositionAve(i,rpm,5)
        

        x = x - x_turnTableAxis
        y = y - y_turnTableAxis
        
        if cupType == "Medium":
            r_cCup = r_cupMedium
            color = [255,0,20]
        else:
            r_cCup = r_cupLarge
            color = [0,255,20]
        c_cent = (cent[0]+int(round(y,0)),cent[1]+int(round(x,0)))
        cv2.circle(img, c_cent, 10, color, -1)
        cv2.circle(img, c_cent, 2, (0,0,0), -1)
    """

    cv2.imshow('Average Cups',img)

def clusterCup(rpm,SplitTend=0.5,tlag=0.1):
    d_table = 255
    r_cupLarge = 45
    r_cupMedium = 39

    #initalise image
    img = np.zeros((300,300,3),dtype=np.uint8)
    si = img.shape
    cent = (si[0]/2,si[1]/2)
    cv2.circle(img, cent, d_table/2, [255,255,255])

    currentCupsPos = []
    currentCupsType = {}
    #raw cups
    for i in xrange(len(cupInitTime)):
        x,y,cupType = getCupPosition(i,rpm)

        currentCupsPos.append(np.array([x,y]))
        currentCupsType[str(round(x,2))+str(round(y,2))]=cupType
        
        x = x - x_turnTableAxis
        y = y - y_turnTableAxis
        
        if cupType == "Medium":
            r_cCup = r_cupMedium
            color = [255,0,0]
        else:
            r_cCup = r_cupLarge
            color = [0,255,0]
        c_cent = (cent[0]+int(round(y,0)),cent[1]+int(round(x,0)))
        cv2.circle(img, c_cent, r_cCup, color)
        cv2.circle(img, c_cent, 1, color)


    if len(currentCupsPos)>10:
        # convert to np.float32
        Z = currentCupsPos[:]
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


        #closeCenters = []
        #closeSegregated = []
        #for i in xrange(groups):
#            for j in xrange(i,groups):
#                if i!=j and sqrt((centers[i][0]-centers[j][0])**2+(centers[i][1]-centers[j][1])**2)<(2*r_cupMedium):
                    
        """
        # Combine overlapping cups, too hard
        closeCenters = []
        for i in xrange(groups):
            for j in xrange(i,groups):
                if i<>j and sqrt((centers[i][0]-centers[j][0])**2+(centers[i][1]-centers[j][1])**2)<(2*r_cupMedium):
                    closeCenters.append([i,j])
        print "closeCenters",closeCenters
        segregatedNewList = []
        centersNewList = []
        popList = []
        newGroups = []
        comboGroup = []
        for pair in closeCenters:
            p0 = pair[0]
            p1 = pair[1]
            #segregatedNewList.append(segregated[pair[0]]+segregated[pair[1]])
            segregatedNewList.append(np.vstack((segregated[p0],segregated[p1])))
            centersNewList.append([(centers[p0][0]+centers[p1][0])/2.,
                                   (centers[p0][1]+centers[p1][1])/2.])
            if (p0 not in popList):
                popList.append(p0)
            if (p1 not in popList):
                popList.append(p1)

            #Check if already put in a group
            if (len(newGroups) == 0):
                newGroups.append(pair)
            for i in xrange(len(closeCenters)):                
                comboGroup = [group for group in newGroups if any([p0 in group, p1 in group])]
                print "comboGroup",comboGroup
                if len(comboGroup) > 0:
                    checkSet = set(itertools.chain.from_iterable(comboGroup))
                    print newGroups[i]," ",checkSet
                    newGroups[i] = (list(set(newGroups[i])|checkSet))
                else:
                    newGroups.append(pair)
                '''if p0 in newGroups[i] and p1 not in newGroups[i]:
                    print "newGroups[i] before:",newGroups[i]
                    newGroups[i].append(p1)
                    #newGroups[i] = newGroups[i].append(p1)
                    print "newGroups[i] after:",newGroups[i]
                elif p1 in newGroups[i] and p0 not in newGroups[i]:
                    newGroups[i].append(p0)
                elif p1 in newGroups[i] and p0 in newGroups[i]:
                    continue
                else:
                    newGroups.append(pair)
                    '''
        print "newGroups",newGroups                       

        #popList=(list(set(popList))).sort(reverse=True)
        popList.sort(reverse=True)
        while (len(popList) > 0):
            popVal = popList.pop(0)
            groups -= 1
            segregated.pop(popVal)
            centers.pop(popVal)
        segregated = segregated + segregatedNewList
        centers = centers + centersNewList
        groups += len(centersNewList)
        #print "popList",popList
        
        """
                
        global cupAveTime
        cupAveTime = time.time()-t0-tlag

        finalCupsTemp = []
        
        for i in xrange(groups):
            segregatedCupTypes = []
            [x,y] = centers[i]
            xWorld = x
            yWorld = y
            x = x - x_turnTableAxis
            y = y - y_turnTableAxis

            default = None
            for j in segregated[i]:
                segregatedCupTypes.append(currentCupsType.get(str(round(j[0],2))+str(round(j[1],2)), default))
            LargeCount = segregatedCupTypes.count('Large')
            MediumCount = segregatedCupTypes.count('Medium')
            if LargeCount>MediumCount:
                ModalCupType = 'Large'
                centColor = [0,255,0]
                r_cCup = r_cupLarge
            else:
                ModalCupType = 'Medium'
                centColor = [255,0,0]
                r_cCup = r_cupMedium

            c_cent = (cent[0]+int(round(y,0)),cent[1]+int(round(x,0)))
            cv2.circle(img, c_cent, 10, centColor, -1)
            cv2.circle(img, c_cent, r_cCup, centColor,thickness=5)
            cv2.circle(img, c_cent, 2, (0,0,0), -1)
            finalCupsTemp.append([xWorld,yWorld,0,ModalCupType])
        global cupAveInitPos
        cupAveInitPos = finalCupsTemp
    
            
            
    cv2.imshow('Cups',img)

def pickNearestCup(reqCupType,rpm,delay=5):
    futureCups = []
    for i in xrange(len(cupAveInitPos)):
        x,y,cupType,x0,y0,cupAveTimeTemp = getCupPositionAve(i,rpm,delay)
        completeDistList = []
        for i in xrange(len(cupCompletedPos)):
            temp = cupCompletedPos[i]
            [x0,y0,rpm,delayTime,cupAveTimeTemp1] = temp
            xComp,yComp = getCupPositionAtTime(x0,y0,rpm,0,cupAveTimeTemp1)
            completeDistList.append(sqrt((xComp-x)**2+(yComp-y)**2))
        minCompleteLit = 100
        if len(completeDistList)>0:
            minCompleteLit = min(completeDistList)
        if cupType == reqCupType and minCompleteLit>50:
            x0 = x - x_turnTableAxis
            y0 = y - y_turnTableAxis
            theta0 = atan2(x0,y0)
            futureCups.append([theta0,x,y,x0,y0,cupAveTimeTemp,rpm])

    contenderCups = []
    for i in futureCups:
        #if radians(165)<i[0]<radians(180) or radians(-180)<i[0]<radians(-75):
        if radians(-180)<i[0]<radians(-90):
            contenderCups.append(i)

    contenderCups.sort(key=lambda x: (x[0]+radians(360) % radians(360)))

    if len(contenderCups)>0:
        return contenderCups[0]
    else:
        return None

def switch_vacuum(ser,state):
    if state == 1:
        ser.write('o')
    elif state == 0:
        ser.write('x')
    else:
        return

def getCupPositionAtTime(x0,y0,rpm,tAhead,cupAveTimeTemp):
    #Extract inital global variables
    theta0 = atan2(x0,y0)
    r = sqrt(x0**2+y0**2)
    t = time.time()-t0-cupAveTimeTemp
    theta = rpm*(pi/30.)*(t+tAhead)+theta0
    x_circle = r*sin(theta) + x_turnTableAxis
    y_circle = r*cos(theta) + y_turnTableAxis
    return x_circle,y_circle

def loop(rpm):
    cv2.destroyAllWindows()
    tkpTdList = SIFTLoadTemplates()
    iterationCount = 0
    while True:
        MatchAllCluster(iterationCount,0,tkpTdList, maxdist=80, filtparam=1.0, SplitTend = 0.5, ROI = 1, drawnoncups = 1)
        clusterCup(rpm,SplitTend=1.2,tlag=0)
        visualiseCupAve(rpm,tAhead=5)
        cv2.waitKey(1)
        iterationCount += 1


def pickupAndFill(x,y,sleeptime,x0,y0,cupAveTimeTemp,rpm):
    global ser
    cupCompletedPos.append([x0,y0,rpm,-1*sleeptime-0.5,cupAveTimeTemp])
    sleeptime2 = 3
    coaster = transformWorldToBilly(-330,90,20)
    midpoint = transformWorldToBilly(-180,50,110)
    [xb,yb,zb] = transformWorldToBilly(x,y,140)
    setDesired(xb,yb,zb)
    switch_vacuum(ser,1)
    cv2.waitKey(int(sleeptime*1000))
    switch_vacuum(ser,1)
    setDesired(xb,yb,10)
    cv2.waitKey(500)
    setDesired(xb,yb,-30)
    cv2.waitKey(500)
    setDesired(xb,yb,140)
    cv2.waitKey(2000)
    setDesired(midpoint[0],midpoint[1],midpoint[2])
    cv2.waitKey(2*1000)
    setDesired(coaster[0],coaster[1],coaster[2])
    cv2.waitKey(5*1000)
    setDesired(midpoint[0],midpoint[1],midpoint[2])
    cv2.waitKey(500)
    xnew,ynew = getCupPositionAtTime(x0,y0,rpm,sleeptime2,cupAveTimeTemp)
    xnewtable = xnew - x_turnTableAxis
    ynewtable = ynew - y_turnTableAxis
    theta0 = atan2(xnewtable,ynewtable)
    while not (radians(-180)<theta0<radians(-90)):
        xnew,ynew = getCupPositionAtTime(x0,y0,rpm,sleeptime2,cupAveTimeTemp)
        xnewtable = xnew - x_turnTableAxis
        ynewtable = ynew - y_turnTableAxis
        theta0 = atan2(xnewtable,ynewtable)
        cv2.waitKey(20)
    [xnew,ynew,znew] = transformWorldToBilly(xnew,ynew,140)
    setDesired(xnew,ynew,150)
    cv2.waitKey(int((sleeptime2- 1.2 - 0.5)*1000))
    switch_vacuum(ser,0)
    cv2.waitKey(100)
    switch_vacuum(ser,0)
    cv2.waitKey(1200)
    setDesired(xnew,ynew,50)
    cv2.waitKey(500)
    setDesired(xnew,ynew,20)
    cv2.waitKey(2*1000)
    setDesired(xnew,ynew,140)

def playAudio():
    audioFile = Sound.AudioFile("Train.wav")
    audioFile.play()
    audioFile.close()


if __name__== '__main__':
    menu = [3,[(1,2,0,1,0,0),(1,0,2,0,0,1),(2,1,0,1,0,0)]]
    numDrinks = menu[0]
    drinks = menu[1]
    print "Number of drinks: " + str(numDrinks) + "\n"
    orderedDrinks = []
    for e in drinks:
        if e[5] == 0:
            orderedDrinks.append(e)
        else:
            orderedDrinks.insert(0,e)
    for i,e in enumerate(orderedDrinks):
        print "Order " + str(i + 1)
        print "Cupsize: " + ("Medium" if e[0] == 1 else "Large")
        print "Number of coffee sachets: " + str(e[1])
        print "Number of teabags: " + str(e[2])
        print "Number of sugars: " + str(e[3])
        print "Espresso: " + ("Yes" if e[4] == 1 else "No")
        print "Urgent: " + ("Yes" if e[5] == 1 else "No")
        print ""
    print ""
    print "---------------------------------"
    print "---------------------------------"
    print ""
    #rpm = 60/31.92
    rpm = 60/28.55
    thread.start_new_thread(loop,(tuple([rpm])))
    #FrameFind()

    ser = serial.Serial('/dev/tty.usbmodem14141', 115200)
    mx,my,mz = initNXT()
    setDesired(0,0,150)
    thread.start_new_thread(mainMotorLoop, (mx,my,mz))
    """while True:
        MatchAllCluster(iterationCount,0,tkpTdList, maxdist=80, filtparam=1.0, SplitTend = 0.5, ROI = 1, drawnoncups = 1)
        clusterCup(rpm,SplitTend=1.0,tlag=0)
        visualiseCupAve(rpm,tAhead=5)
        cv2.waitKey(1)
        iterationCount += 1

        if iterationCount % 5:
            print pickNearestCup("Medium",rpm,delay=0)"""
    cv2.waitKey(20000)
  
    waitDelay = 3
    #pickupAndFill(-183,213,5)
    for e in orderedDrinks:
        if(e[0] == 2):
            orderSize = "Large"
        else:
            orderSize = "Medium"
        print "Next order:"
        print "Cupsize: " + orderSize
        print "Number of coffee sachets: " + str(e[1])
        print "Number of teabags: " + str(e[2])
        print "Number of sugars: " + str(e[3])
        print ""
        temp = pickNearestCup(orderSize,rpm,delay=waitDelay)
        while temp == None:
            cv2.waitKey(500)
            temp = pickNearestCup(orderSize,rpm,delay=waitDelay)
        [ang, x, y, x0,y0,cupAveTimeTemp,rpm] = temp
        pickupAndFill(x,y,waitDelay-0.5,x0,y0,cupAveTimeTemp,rpm)
        print "Order complete"
        print ""
        print "---------------------------------"
        print ""
        thread.start_new_thread(playAudio,())
        cv2.waitKey(5*1000)
        
    
        

    
    
        

    
