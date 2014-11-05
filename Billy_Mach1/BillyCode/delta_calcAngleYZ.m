function theta = delta_calcAngleYZ(x0, y0, z0)
    parameters2;
    %theta = false;
    y1 = -0.5 * 0.57735 * f; %// f/2 * tg 30
    y0 = y0 - 0.5 * 0.57735 * e;   % // shift center to edge
    %// z = a + b*y
    a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2*z0);
    b = (y1-y0)/z0;
    %// discriminant
    d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf); 
    if (d < 0) 
        return %// non-existing point
    end
    yj = (y1 - a*b - sqrt(d))/(b*b + 1);% // choosing outer point
    zj = a + b*yj;
    if (yj>y1) 
        theta = 180.0*atan(-zj/(y1 - yj))/pi + 180;
    else
        theta = 180.0*atan(-zj/(y1 - yj))/pi + 0;
    end
    return
end
 %// inverse kinematics: (x0, y0, z0) -> (theta1, theta2, theta3)
 %// returned status: 0=OK, -1=non-existing position
