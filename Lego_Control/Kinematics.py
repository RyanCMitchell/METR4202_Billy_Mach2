"This files containes the forward and inverse kinematics relating to the robot"
from math import sqrt, tan, atan, degrees, pi, cos, sin, radians

#define the constants
rf = 143 #142.5 bicep length
re = 213 #154.4 forarm length
f = 154.4*2 #280.51 top sidelength
e = 32.5*2 #93.53 base sidelength
t = (f - e)*tan(radians(30))/2
frameAngle = 33
measuredAngle = 90
initAng = measuredAngle-frameAngle


def cosd(x):
    return cos(radians(x))

def sind(x):
    return sin(radians(x))

def tand(x):
    return tan(radians(x))

def delta_calcAngleYZ(x0, y0, z0):

    #theta = false
    y1 = -0.5 * 0.57735 * f #// f/2 * tg 30
    y0 = y0 - 0.5 * 0.57735 * e   # // shift center to edge

    #// z = a + b*y
    a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2.0*z0)
    b = (y1-y0)/z0

    #// discriminant
    d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf)

    if (d < 0.0):
        return None#// non-existing point

    yj = (y1 - a*b - sqrt(d))/(b*b + 1)# // choosing outer point
    zj = a + b*yj

    if (yj>y1):
        theta = 180.0*atan(-zj/(y1 - yj))/pi + 180.0
    else:
        theta = 180.0*atan(-zj/(y1 - yj))/pi + 0.0
    return theta

 #// inverse kinematics: (x0, y0, z0) -> (theta1, theta2, theta3)
 #// returned status: 0=OK, -1=non-existing position

def delta_calcInverse(x0, y0, z0):
    theta1 = delta_calcAngleYZ(x0, y0, z0)
    theta2 = delta_calcAngleYZ(x0*cosd(120) + y0*sind(120), y0*cosd(120)-x0*sind(120), z0)  #// rotate coords to +120 deg
    theta3 = delta_calcAngleYZ(x0*cosd(120) - y0*sind(120), y0*cosd(120)+x0*sind(120), z0)  #// rotate coords to -120 deg
    return theta1, theta2, theta3

def forwardKin2( theta1, theta2, theta3 ):
    dtr = pi/180
    theta1 = theta1*dtr
    theta2 = theta2*dtr
    theta3 = theta3*dtr
    y1 = -(t + rf*cos(theta1))
    z1 = -rf*sin(theta1)
    y2 = (t + rf*cos(theta2))*sind(30)
    x2 = y2*tand(60)
    z2 = -rf*sin(theta2)
    y3 = (t + rf*cos(theta3))*sind(30)
    x3 = -y3*tand(60)
    z3 = -rf*sin(theta3)
    dnm = (y2-y1)*x3-(y3-y1)*x2
    w1 = y1*y1 + z1*z1
    w2 = x2*x2 + y2*y2 + z2*z2
    w3 = x3*x3 + y3*y3 + z3*z3
    # x = (a1*z + b1)/dnm
    a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
    b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0
    # y = (a2*z + b2)/dnm
    a2 = -(z2-z1)*x3+(z3-z1)*x2
    b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0
    # a*z^2 + b*z + c = 0
    a = a1*a1 + a2*a2 + dnm*dnm
    b = 2*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
    c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)
    # discriminant
    d = b*b - 4.0*a*c
    if (d < 0):
        return None#// non-existing point
    z0 = -0.5*(b+sqrt(d))/a
    x0 = (a1*z0 + b1)/dnm
    y0 = (a2*z0 + b2)/dnm
    return x0, y0, z0

def correctFrameAngle(theta1, theta2, theta3):
    theta1 = theta1-frameAngle
    theta2 = theta2-frameAngle
    theta3 = theta3-frameAngle
    return theta1,theta2,theta3

def correctMotorAngle(a0,b0,c0):
    #Subtracts desried motor position from current
    a = a0 - initAng
    b = b0 - initAng
    c = c0 - initAng
    return a,b,c

def correctPos(x0, y0, z0):
    #Converts from input coordinates to Billy coordinates
    dx,dy,dz = forwardKin2(initAng,initAng,initAng)
    x = x0+dx
    y = y0+dy
    z = z0+dz
    return x,y,z

if __name__=='__main__':
    #motor centre 8.5cm radially from billy centre

    
    #a,b,c = delta_calcInverse(0,0,1)
    print a,b,c
    #print forwardKin2( a, b, c )
    #FindExtends(32,32)
    #ErrorSurf(n=10)

