function [theta1, theta2, theta3] = delta_calcInverse_design(x0, y0, z0, rf, re, h) 
    f = 154.4*2; %280.51;
    e = 46.3*2; %93.53;
    t = (f - e)*tand(30)/2;
    z0 = z0 - h;
    theta1 = delta_calcAngleYZ(x0, y0, z0);
    theta2 = delta_calcAngleYZ(x0*cosd(120) + y0*sind(120), y0*cosd(120)-x0*sind(120), z0);  %// rotate coords to +120 deg
    theta3 = delta_calcAngleYZ(x0*cosd(120) - y0*sind(120), y0*cosd(120)+x0*sind(120), z0);  %// rotate coords to -120 deg
end