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

    time.sleep(0.5)
    #query until access is given then read tachos
    """
    A = [0]; B = [0]; C = [0];
    while 1:
        x1 = mx.get_tacho()
        if x1.tacho_count <> x0.tacho_count:
            A.append((mx.get_tacho().tacho_count)/5.0)
            B.append((my.get_tacho().tacho_count)/5.0)
            C.append((mz.get_tacho().tacho_count)/5.0)
            if A[-1]==A[-2] and B[-1]==B[-2] and C[-1]==C[-2]:
                a1 = A[-1]
                b1 = B[-1]
                c1 = C[-1]
                break
    print a1,b1,c1
    """

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
    
def instructionsmake(a,b,c,power):
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

def mainMotorLoop():
    global motorDesiredArray
    mx,my,mz = initNXT()
    samePosCount = 0
    Ea_old = 0; Eb_old = 0; Ec_old = 0
    while(True):
        [Ad,Bd,Cd,power] = motorDesiredArray
        [Aa,Ba,Ca] = readTacho(mx,my,mz)
        Ea = (Ad-(Aa/5))*5; Eb = (Bd-(Ba/5))*5; Ec = (Cd-(Ca/5))*5
        #print "[Ad,Bd,Cd]: ",[Ad,Bd,Cd]
        #print "[Aa,Ba,Ca]: ",[Aa,Ba,Ca]
        #print "[Ea,Eb,Ec]: ",[Ea,Eb,Ec]
        if(((abs(Ea_old)-abs(Ea))<10)and((abs(Ea_old)-abs(Ea))<10)and((abs(Ea_old)-abs(Ea))<10)):
            samePosCount+=1
        else:
            samePosCount = 0
        Ea_old = Ea; Eb_old = Eb; Ec_old = Ec
        
        print "Desired", Ad,Bd,Cd
        print "Actual ", Aa,Ba,Ca
        print "Error  ", Ea,Eb,Ec
        if(samePosCount < 5):
            runNxt(Ea,Eb,Ec,power,mx,my,mz)
    
def setDesired(x0,y0,z0,power):
    print " "
    x,y,z = correctPos(x0, y0, z0)
    #print "x,y,z: ",x,y,z
    a0,b0,c0 = delta_calcInverse(x, y, z)
    #print "a0,b0,c0: ",a0,b0,c0
    a,b,c = correctMotorAngle(a0,b0,c0)
    #print "a,b,c: ",a,b,c
    global motorDesiredArray
    motorDesiredArray = [-a,-b,-c,power]

    

    

if __name__=='__main__':
    #dynamixel centre 8.5cm radially from billy centre
    #motor A upper support 32deg to horizontal
    #motor B upper support
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
    thread.start_new_thread(mainMotorLoop, ())
    #print motorDesiredArray

    # now, down here we should be able to change setDesired and see
    # the change in the motors (via the child thread loop)
    setDesired(0,0,0,60)
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
    """
   
    """
    """
    time.sleep(3.5)
    setDesired(150,0,0,80)
    time.sleep(0.5)
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
    setDesired(100,0,-0,80)
    time.sleep(0.5)
    setDesired(100,0,50,80)
    time.sleep(0.5)
    setDesired(0,0,50,80)
    time.sleep(0.5)
    setDesired(0,0,0,80)
    """

    
    
