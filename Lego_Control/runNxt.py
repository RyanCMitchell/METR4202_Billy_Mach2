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

    
    #query until access is given then read tachos
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
    [Ad,Bd,Cd,power] = motorDesiredArray
    [Aa,Ba,Ca] = readTacho(mx,my,mz)
    Ea = (Ad-Aa)*5; Eb = (Bd-Ba)*5; Ec = (Cd-Ca)*5
    print "Desired", Ad,Bd,Cd
    print "Actual ", Aa,Ba,Ca
    print "Error  ", Ea,Eb,Ec
    
    
def setDesired(x0,y0,z0,power):
    x,y,z = correctPos(x0, y0, z0)
    a0,b0,c0 = delta_calcInverse(x, y, z)
    a,b,c = correctMotorAngle(a0,b0,c0)
    print a,b,c
    global motorDesiredArray
    motorDesiredArray = [a,b,c,power]

    

    

if __name__=='__main__':
    #dynamixel centre 8.5cm radially from billy centre
    #motor A upper support 32deg to horizontal
    #motor B upper support
    motorDesiredArray = [0,0,0,80]
    """
    mx,my,mz = initNXT()
    a = 2.
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
    setDesired(0,0,100,60)
    print motorDesiredArray
    mainMotorLoop()
    
    
    
    
    
