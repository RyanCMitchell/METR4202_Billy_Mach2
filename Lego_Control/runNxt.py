#Script to control a NXT 2-axis CNC "Pancake maker"
#Illustrates controlling more than one motor at the same time without trying to
#sync them. Uses the thread module.
#Written 2/3/11 by Marcus Wanner
#
#For more info and warnings see:
#http://groups.google.com/group/nxt-python/browse_thread/thread/f6ef0865ae768ef
from Kinematics import *
import numpy as np
import nxt, thread, time, serial
motorDesiredArray = [0,0,0,80]

<<<<<<< HEAD
def switch_vacuum(ser,state):
    
    if state == 1:
        ser.write('o')
    elif state == 0:
        ser.write('x')
    else:
        return

=======
>>>>>>> 58bf3309326707017afc00a4b58cc724bbf4c7e0
def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)

def initNXT():
    LegoBrick = nxt.find_one_brick()
    mx = nxt.Motor(LegoBrick, nxt.PORT_A)
    my = nxt.Motor(LegoBrick, nxt.PORT_B)
    mz = nxt.Motor(LegoBrick, nxt.PORT_C)
    return mx,my,mz

def runNxt(a,b,c,power,mx,my,mz):
    #create a list of instructions
    instructions = instructionsmake(a,b,c,power)

    #get tach readings before running
    x0 = mx.get_tacho()
    y0 = my.get_tacho()
    z0 = mz.get_tacho()
    motors = [mx,my,mz]

    def turnmotor(m, power, degrees):
            m.turn(power, degrees)

    #here are the instructions...
    #the first value is the time to start the instruction
    #the second is the axis (0 for x, 1 for y, 2 for z)
    #the third is the power
    #the fourth is the degrees
    #it's probably not a good idea to run simultaneous turn
    #functions on a single motor, so be careful with this

    def runinstruction(i):
            motorid, speed, degrees = i
            #THIS IS THE IMPORTANT PART!
            thread.start_new_thread(
                    turnmotor,
                    (motors[motorid], speed, degrees))

    #run motor
    seconds = 0
    for i in instructions:
        runinstruction(i[1:])

    #time.sleep(0.1)
    #query until access is given then read tachos
    while (not(mx.isFinished) or not(my.isFinished) or not(mz.isFinished)):
        pass
    #print "Would have gone on"
    #time.sleep(0.1)
    
    """
    while withinLimit == False:
        if x1<>x0.tacho_count or y1<>y0.tacho_count or z1<>z0.tacho_count:
            print "1st"
            A.append(x1)
            B.append(y1)
            C.append(y1)
            if len(A) > 1:
                print "2nd"
                if (abs(A[-1])-abs(A[-2]) < tachoLimit) and (abs(B[-1])-abs(B[-2]) < tachoLimit) and (abs(C[-1])-abs(C[-2]) < tachoLimit):
                    print "3rd"
                    withinLimit = True
            else: break
    print "Tacho count: ", A[-1], B[-1], C[-1]"""

    """
    A = [0]; B = [0]; C = [0];
    while 1:
        x1 = mx.get_tacho()
        if x1.tacho_count <> x0.tacho_count:
            A.append((mx.get_tacho().tacho_count))
            B.append((my.get_tacho().tacho_count))
            C.append((mz.get_tacho().tacho_count))
            if (abs(A[-1])-abs(A[-2])< 2) and (abs(B[-1])-abs(B[-2])< 2) and (abs(C[-1])-abs(C[-2])< 2):
                a1 = A[-1]
                b1 = B[-1]
                c1 = C[-1]
                break
    print a1,b1,c1"""


def readTacho(mx,my,mz):
    return [mx.get_tacho().tacho_count,my.get_tacho().tacho_count,mz.get_tacho().tacho_count]
    """
def resetTacho():
    import nxt
    #retrives current position
    LegoBrick = nxt.find_one_brick()
    mx = nxt.Motor(LegoBrick, nxt.PORT_A)
    my = nxt.Motor(LegoBrick, nxt.PORT_B)
    mz = nxt.Motor(LegoBrick, nxt.PORT_C)

    #defines the current arm position in kinematics coordinates
    motorA0 = (mx.get_tacho().tacho_count)/5.0 + measuredAngle - frameAngle
    motorB0 = (my.get_tacho().tacho_count)/5.0 + measuredAngle - frameAngle
    motorC0 = (mz.get_tacho().tacho_count)/5.0 + measuredAngle - frameAngle

    #saves the position as a numpy array
    MotorPosition = np.array([motorA0,motorB0,motorC0])
    np.save('MotorPosition',MotorPosition)
    """

def instructionsmake2(a,b,c,power):
    dir1 = 1.; dir2 = 1.; dir3 = 1.;
    if a < 0.0:
        dir1 = -1.
    if b < 0.0:
        dir2 = -1.
    if c < 0.0:
        dir3 = -1.
    instructions = (
                    [0, 0, dir1*power, abs(a)],
                    [0, 1, dir2*power, abs(b)],
                    [0, 2, dir3*power, abs(c)],
            )
    return instructions


def returnToZero():
    [a,b,c] = readTacho()
    while abs(a)>4 or abs(b)>4 or abs(c)>4:
        print [a,b,c]
        instructions = instructionsmake(-a/5.,-b/5.,-c/5.,50)
        runNxt(instructions)
        time.sleep(1)
        [a,b,c] = readTacho()

def mainMotorLoop(mx,my,mz):
    global motorDesiredArray
    #mx,my,mz = initNXT()
    samePosCount = 0
    tol = 5
    Ea_old = 0; Eb_old = 0; Ec_old = 0
    Ad_old = 0; Bd_old = 0; Cd_old = 0;
    while(True):
        flag=1
        multiplier = 1
        [Ad,Bd,Cd,power] = motorDesiredArray
        [Aa,Ba,Ca] = readTacho(mx,my,mz)
        Ea = (Ad-(Aa/5))*5; Eb = (Bd-(Ba/5))*5; Ec = (Cd-(Ca/5))*5
        #print "[Ad,Bd,Cd]: ",[Ad,Bd,Cd]
        #print "[Aa,Ba,Ca]: ",[Aa,Ba,Ca]
        #print "[Ea,Eb,Ec]: ",[Ea,Eb,Ec]
        if((abs(Ea_old-Ea)<10)and(abs(Eb_old-Eb)<10)and(abs(Ec_old-Ec)<10)):
            samePosCount+=1
        else:
            samePosCount = 0
        Ea_old = Ea; Eb_old = Eb; Ec_old = Ec
        if(Ad == Ad_old and Bd == Bd_old and Cd == Cd_old):
            multiplier = 0.8
        Ad_old = Ad; Bd_old = Bd; Cd_old = Cd;
        if (abs(Ea)<6)and(abs(Eb)<6)and(abs(Ec)<6):
            flag = 0
        #print "Desired", Ad*5,Bd*5,Cd*5
        #print "Actual ", Aa,Ba,Ca
        #print "Error  ", Ea,Eb,Ec
        if((samePosCount < 5)and flag):
            runNxt(multiplier*Ea,multiplier*Eb,multiplier*Ec,power,mx,my,mz)

        
def setDesired(x0,y0,z0,power=False):
    x,y,z = correctPos(x0, y0, z0)
    #print "x,y,z: ",x,y,z
    a0,b0,c0 = delta_calcInverse(x, y, z)
    #print "a0,b0,c0: ",a0,b0,c0
    a,b,c = correctMotorAngle(a0,b0,c0)
    #print "a,b,c: ",a,b,c
    global motorDesiredArray
    motorDesiredArray = [-a,-b,-c,power]

def transformWorldToBilly(xworld,yworld,zworld):
    xworld = xworld + 176 + 55
    yworld = yworld - 235 + 65
    xbilly = xworld*cosd(-30) - yworld*sind(-30)
    ybilly = xworld*sind(-30) + yworld*cosd(-30)
    return [xbilly,-ybilly,zworld]

def rotateBillyFrame(x,y,z):
    return

def instructionsmake(degx,degy,degz,power):
    if(power==False):
        time = 1.5
        minSpeed = 30
        cutOff = minSpeed*time
        if abs(degx) < cutOff:
            if degx < 0:
                speed1 = -minSpeed
            else:
                speed1 = minSpeed
        elif abs(degx) > 99:
            if degx < 0:
                speed1 = -99
            else:
                speed1 = 99
        else:
            speed1 = int(degx/time)
            
        if abs(degy) < cutOff:
            if degy < 0:
                speed2 = -minSpeed
            else:
                speed2 = minSpeed
        elif abs(degy) > 99:
            if degy < 0:
                speed2 = -99
            else:
                speed2 = 99
        else:
            speed2 = int(degy/time)
            
        if abs(degz) < cutOff:
            if degz < 0:
                speed3 = -minSpeed
            else:
                speed3 = minSpeed
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
        instructions = (
                        [0, 0, speed1, x],
                        [0, 1, speed2, y],
                        [0, 2, speed3, z],
                )
            
        return instructions
    else:
        return instructionsmake2(degx,degy,degz,power)
<<<<<<< HEAD

def kinect2Billy(x,y,z):
    # adjust for left hand rule kinematics (already with corrected z)

=======

def kinect2Billy(x,y,z):
    # adjust for left hand rule kinematics (already with corrected z)

>>>>>>> 58bf3309326707017afc00a4b58cc724bbf4c7e0
    return newx,newy,newz

if __name__=='_main__':
    #dynamixel centre 8.5cm radially from billy centre
    #motor A upper support 32deg to horizontal
    #motor B upper support
    mx,my,mz = initNXT()
    ser = serial.Serial('/dev/tty.usbmodem1411', 115200)
    """
    mx,my,mz = initNXT()
    a = 5.
    b = 0.
    c = 0.
    power = 50
    runNxt(a,b,c,power,mx,my,mz)
    """
    #resetTacho()
    #print readTacho()
    #returnToZero()

    """
    x = 0.
    y = 0.
    z = -50.
    power = 50
    moveRel(x,y,z,power)
    """

    # make the motor thread
    thread.start_new_thread(mainMotorLoop, (mx,my,mz))
    #print motorDesiredArray

    # now, down here we should be able to change setDesired and see
    # the change in the motors (via the child thread loop)
    setDesired(0,0,0)
    """
    time.sleep(3.5)
    #run in a circle
    t0 = time.time()
    while True:
        t = time.time()-t0
        rpm = 10
        r = 50
        theta = rpm*(pi/30.)*t
        x_circle = r*cos(theta)
        y_circle = r*sin(theta)
        print "x: ",x_circle," y: ",y_circle
        setDesired(x_circle+85,y_circle-40,0)
        time.sleep(0.2)
    """
    

    """
    #step out in x (shit)
    x_lin = 0
    while x_lin<200:
        t = time.time()-t0
        x_dot = 8
        x_lin = x_dot*t
        print " "
        print "x: ",x_lin
        print " "
        setDesired(x_lin,0,0,50)
        time.sleep(0.1)
    """
    #(x,y,z) =  kinect2Billy(100,0,0)
    
    time.sleep(5)
    [x,y,z] = transformWorldToBilly(-236,148,140)
    setDesired(x,y,z)
    time.sleep(2)
    [x,y,z] = transformWorldToBilly(-181,213,140)
    setDesired(x,y,z)
    time.sleep(4)
    switch_vacuum(ser,1)
    time.sleep(1)
    [x,y,z] = transformWorldToBilly(-181,213,-35)
    setDesired(x,y,z)
    time.sleep(1)
    [x,y,z] = transformWorldToBilly(-181,213,130)
    setDesired(x,y,z)
    time.sleep(5)
    setDesired(0,0,0)
    switch_vacuum(ser,0)
    

    
    # raw input value testing
    """while(1):
        move = raw_input("x y z?: ")
        move = move.split(' ')
        if(move[0] == "q"):
            break
        setDesired(int(move[0]),int(move[1]),int(move[2]))
        time.sleep(2)"""
        
 
    #time.sleep(10)
    #setDesired(130, 0, 0)
    #time.sleep(10)
    #setDesired(0, 0, 0)
    
