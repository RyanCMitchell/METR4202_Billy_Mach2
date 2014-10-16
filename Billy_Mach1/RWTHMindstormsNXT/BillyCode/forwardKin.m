function [ z0, x0, y0 ] = forwardKin( theta1, theta2, theta3 )

% Load the parameters
parameters;

y1 = -(R + L1*cosd(theta1));
z1 = -L1*sind(theta1);
 
y2 = (R + L1*cosd(theta2))*sind(30);
x2 = y2*tand(60);
z2 = -L1*sind(theta2);
 
y3 = (R + L1*cosd(theta3))*sind(30);
x3 = -y3*tand(60);
z3 = -L1*sind(theta3);
 
dnm = (y2 - y1)*x3 - (y3 - y1)*x2;
 
w1 = y1^2 + z1^2;
w2 = x2^2 + y2^2 + z2^2;
w3 = x3^2 + y3^2 + z3^2;
     
% x = (a1*z + b1);
a1 = ((z2 - z1)*(y3 - y1) - (z3 - z1)*(y2 - y1))/dnm;
b1 = -((w2 - w1)*(y3 - y1) - (w3 - w1)*(y2 - y1))/(2*dnm);
 
% y = (a2*z + b2);
a2 = -((z2 - z1)*x3 - (z3 - z1)*x2)/dnm;
b2 = ((w2 - w1)*x3 - (w3 - w1)*x2)/(2*dnm);
 
% a*z^2 + b*z + c = 0
a = a1^2 + a2^2 + 1;
b = 2*(a1*b1 + a2*(b2 - y1) - z1);
c = b1^2 + (b2 - y1)^2 + z1^2 - L2^2;
  
% determinant
 d = b^2 - 4.0*a*c;
     if (d < 0) 
         return
     end;
 
z0 = -(-b + sqrt(d))/(2*a);
x0 = (-a1*z0 + b1);
y0 = (-a2*z0 + b2);

end

