#Script to control a NXT 2-axis CNC "Pancake maker"
#Illustrates controlling more than one motor at the same time without trying to
#sync them. Uses the thread module.
#Written 2/3/11 by Marcus Wanner
#
#For more info and warnings see:
#http://groups.google.com/group/nxt-python/browse_thread/thread/f6ef0865ae768ef
from Kinematics import *
import numpy as np
import nxt, thread, time
motorDesiredArray = [0,0,0,80]

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

    print "mx Tacho: ", mx.get_tacho().tacho_count
    time.sleep(0.1)
    print mx._get_new_state().mode
    time.sleep(0.5)
    print mx._get_new_state().mode
    #query until access is given then read tachos

    A = []; B = []; C = [];
    withinLimit = False
    tachoLimit = 2
    x1 = mx.get_tacho().tacho_count
    y1 = my.get_tacho().tacho_count
    z1 = mz.get_tacho().tacho_count
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
    while(True):
        flag=1
        [Ad,Bd,Cd,power] = motorDesiredArray
        [Aa,Ba,Ca] = readTacho(mx,my,mz)
        Ea = (Ad-(Aa/5))*5; Eb = (Bd-(Ba/5))*5; Ec = (Cd-(Ca/5))*5
        #print "[Ad,Bd,Cd]: ",[Ad,Bd,Cd]
        #print "[Aa,Ba,Ca]: ",[Aa,Ba,Ca]
        #print "[Ea,Eb,Ec]: ",[Ea,Eb,Ec]
        if((abs(Ea_old-Ea)<10)and(abs(Ea_old-Ea)<10)and(abs(Ea_old-Ea)<10)):
            samePosCount+=1
        else:
            samePosCount = 0
        Ea_old = Ea; Eb_old = Eb; Ec_old = Ec
        if (abs(Ea)<5)and(abs(Eb)<5)and(abs(Ec)<5):
            flag = 0
        #print "Desired", Ad*5,Bd*5,Cd*5
        #print "Actual ", Aa,Ba,Ca
        #print "Error  ", Ea,Eb,Ec
        if((samePosCount < 10)and flag):
            runNxt(Ea,Eb,Ec,power,mx,my,mz)

def setDesired(x0,y0,z0,power=False):
    print " "
    x,y,z = correctPos(x0, y0, z0)
    #print "x,y,z: ",x,y,z
    a0,b0,c0 = delta_calcInverse(x, y, z)
    #print "a0,b0,c0: ",a0,b0,c0
    a,b,c = correctMotorAngle(a0,b0,c0)
    #print "a,b,c: ",a,b,c
    global motorDesiredArray
    motorDesiredArray = [-a,-b,-c,power]

def transformWorldToBilly(x,y,z):
    A = 1
    xnew = 1


def instructionsmake(degx,degy,degz,power):
    if(power==False):
        
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
        instructions = (
                        [0, 0, speed1, x],
                        [0, 1, speed2, y],
                        [0, 2, speed3, z],
                )
            
        return instructions
    else:
        return instructionsmake2(degx,degy,degz,power)



if __name__=='__main__':
    #dynamixel centre 8.5cm radially from billy centre
    #motor A upper support 32deg to horizontal
    #motor B upper support
    mx,my,mz = initNXT()
    print dir(mx)
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
        rpm = 2
        r = 50
        theta = rpm*(pi/30.)*t
        x_circle = r*cos(theta)
        y_circle = r*sin(theta)
        print "x: ",x_circle," y: ",y_circle
        setDesired(x_circle+85,y_circle-40,0,100)
        time.sleep(0.1)
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

    
    """time.sleep(3.5)
    setDesired(150,0,0,80)
    time.sleep(0.5)
    setDesired(-50, 20, -10, 80)
    time.sleep(5)
    setDesired(0,130,0,80)
    time.sleep(0.5)
    setDesired(0,130,0,80)
    time.sleep(0.5)
    setDesired(0,-130,0,80)
    time.sleep(0.5)
    setDesired(0,0,0,80)
    time.sleep(0.5)
    setDesired(0,0,100,80)
    time.sleep(0.5)
    setDesired(-130,0,100,80)
    time.sleep(0.5)
    setDesired(-130,0,0,80)
    time.sleep(0.5)
    setDesired(0,0,100,80)
    time.sleep(0.5)
    setDesired(0,0,0,80)
    time.sleep(0.5)
    setDesired(100,0,0,80)
    time.sleep(0.5)
    setDesired(100,0,50,80)
    time.sleep(0.5)
    setDesired(0,0,50,80)
    time.sleep(0.5)
    setDesired(0,0,0,80)"""

    #time.sleep(3.5)
    #setDesired(150,0,0)
    #time.sleep(1)
    #setDesired(70, -20, -10)
    #time.sleep(1)


    """while(1):
        move = raw_input("x y z?: ")
        move = move.split(' ')
        if(move[0] == "q"):
            break
        setDesired(int(move[0]),int(move[1]),int(move[2]))
        time.sleep(2)"""
        
 

    time.sleep(5)
    setDesired(-130, 0, 0)
    time.sleep(1)
    print mx._get_new_state().mode
    time.sleep(1)
    print mx._get_new_state().mode
    time.sleep(0.5)
    print mx._get_new_state().mode
    time.sleep(1)
    print mx._get_new_state().mode
    time.sleep(1)
    print mx._get_new_state().mode
    setDesired(0, 0, 0)
    time.sleep(5)
    setDesired(130, 0, 0)
    time.sleep(5)
    setDesired(0, 0, 0)
    
