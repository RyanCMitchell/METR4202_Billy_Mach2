from math import degrees, radians, sin, cos, tan, atan, sqrt

# Set the parameters

# Parameters 1
L1 = 142.5
L2 = 232.5
Ra = 280.51
Rb = 93.53
R = (Ra - Rb) * degrees(tan(30))/2

# Parameters 2
rf = 184 #142.5
re = 232 #154.4
f = 154.4 * 2 #280.51
e = 46.3 * 2 #93.53
t = (f - e) * degrees(tan(30))/2


def forwardKin_v1(theta1, theta2, theta3):
    "Performs forward kinematics on the 3 angles supplied and returns 3 coordinates"
    # Makes use of Parameters 1

    y1 = -(R + L1 * degrees(cos(theta1)))
    z1 = -L1 * degrees(sin(theta1))

    y2 = (R + L1 * degrees(cos(theta2))) * degrees(sin(30))
    x2 = y2 * degrees(tan(60))
    z2 = -L1 * degrees(sin(theta2))

    y3 = (R + L1 * degrees(cos(theta3))) * degrees(sin(30))
    x3 = -y3 * degrees(tan(60))
    z3 = -L1 * degrees(sin(theta3))

    dnm = ((y2 - y1) * x3) - ((y3 - y1) * x2)

    w1 = y1 * y1 + z1 * z1
    w2 = x2 * x2 + y2 * y2 + z2 * z2
    w3 = x3 * x3 + y3 * y3 + z3 * z3

    # x = (a1 * z + b1)
    a1 = ((z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)) / dnm
    b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / (2 * dnm)

    # y = (a2 * z + b2)
    a2 = -((z2 - z1) * x3 - (z3 - z1) * x2) / dnm
    b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / (2 * dnm)

    # (a * z^2) + (b * z) + c = 0
    a = a1 * a1 + a2 * a2 + 1
    b = 2 * (a1 * b1 + a2 * (b2 - y1) - z1)
    c = b1 * b1 + (b2 - y1) * (b2 - y1) + z1 * z1 - L2 * L2

    # Calulate the determinant
    d = b * b - 4.0 * a * c;
    if d < 0:
        # non-exisitent point
        return

    z0 = -(-b + sqrt(d)) / (2 * a)
    x0 = (-a1 * z0 + b1)
    y0 = (-a2 * z0 + b2)

    return z0, x0, y0


def forwardKin_v2(theta1, theta2, theta3):
    "Performs forward kinematics on the 3 angles supplied and returns 3 coordinates"
    # Makes use of Parameters 2

    theta1 = radians(theta1)
    theta2 = radians(theta2)
    theta3 = radians(theta3)

    y1 = -(t + rf * cos(theta1))
    z1 = -rf * sin(theta1)

    y2 = (t + rf * cos(theta2)) * degrees(sin(30))
    x2 = y2 * degrees(tan(60));
    z2 = -rf * sin(theta2);

    y3 = (t + rf * cos(theta3)) * degrees(sin(30));
    x3 = -y3 * degrees(tan(60));
    z3 = -rf * sin(theta3);

    dnm = ((y2 - y1) * x3) - ((y3 - y1) * x2)

    w1 = y1**2 + z1 * z1
    w2 = x2 * x2 + y2 * y2 + z2 * z2
    w3 = x3 * x3 + y3 * y3 + z3 * z3

    # x = (a1 * z + b1) / dnm
    a1 = (z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)
    b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2.0

    # y = (a2 * z + b2) / dnm
    a2 = -(z2 - z1) * x3 + (z3 - z1) * x2
    b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / 2.0

    # (a * z^2) + (b * z) + c = 0
    a = a1 * a1 + a2 * a2 + dnm * dnm
    b = 2 * (a1 * b1 + a2 * (b2 - y1 * dnm) - z1 * dnm * dnm)
    c = (b2 - y1 * dnm) * (b2 - y1 * dnm) + b1 * b1 + dnm * dnm * (z1 * z1 - re * re)

    print a, b, c


    # Calculate the discriminant
    d = b * b - 4.0 * a * c
    if d < 0:
        # non-exisitent point
        return

    z0 = -0.5 * (b + sqrt(d)) / a
    x0 = (a1 * z0 + b1) / dnm
    y0 = (a2 * z0 + b2) / dnm

    return z0, x0, y0


def inverseKin(X, Y, Z, motorPos):

    theta = 0

    if motorPos == 0:
        Cx = X
        Cy = Y
    elif motorPos == 120:
        Cx = X * degrees(cos(120)) + Y * degrees(sin(120))
        Cy = -X * degrees(sin(120)) + Y * degrees(cos(120))
    elif motorPos == -120:
        Cx = X * degrees(cos(120)) - Y * degrees(sin(120))
        Cy = X * degrees(sin(120)) + Y * degrees(cos(120))

    # Load the parameters from the parameter file ???
    # parameters *****************

    L3 = sqrt(L2 * L2 - Cx * Cx)

    Ay = -Ra
    PCy= Cy - Rb
    dn = (L1 + sqrt(L2 * L2 - (Ay - PCy) * (Ay - PCy)))


    if abs(Z) <= dn:
        a = (4 * Z * Z + (2 * Ay - 2 * PCy) * (2 * Ay - 2 * PCy))
        b = (-8 * Ay * Z * Z + (4 * Ay - 4 * PCy) * (L1 * L1 - L3 * L3 - Ay * Ay + PCy * PCy + Z * Z))
        c = (4*Ay*Ay*Z*Z - (4*Z*Z) * (L1*L1) + (L1*L1 - L3*L3 - Ay*Ay + PCy*PCy + Z*Z) * (L1*L1 - L3*L3 - Ay*Ay + PCy*PCy + Z*Z))


        D = sqrt(b * b - 4 * a * c)
        By1 = ( -b - D) / (2 * a)
        By2 = ( -b + D) / (2 * a)


        if abs(By1) > abs(By2):
            Bz1 = (By1 * (2 * Ay - 2 * PCy) + L1*L1 - L3*L3 - Ay*Ay + PCy*PCy + Z*Z) / (2 * Z)
            theta = degrees(atan(Bz1/(Ay - By1)))
        else:
            Bz1 = (By2 * (2 * Ay - 2 * PCy) + L1*L1 - L3*L3 - Ay*Ay + PCy*PCy + Z*Z) / (2 * Z)
            theta = degrees(atan(Bz1/(Ay - By2)))

    else:
        # Send an error
        return















