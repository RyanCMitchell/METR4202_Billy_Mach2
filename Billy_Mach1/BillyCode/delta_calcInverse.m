function [theta1, theta2, theta3] = delta_calcInverse(x0, y0, z0)
    theta1 = delta_calcAngleYZ(x0, y0, z0);
    theta2 = delta_calcAngleYZ(x0*cosd(120) + y0*sind(120), y0*cosd(120)-x0*sind(120), z0);  %// rotate coords to +120 deg
    theta3 = delta_calcAngleYZ(x0*cosd(120) - y0*sind(120), y0*cosd(120)+x0*sind(120), z0);  %// rotate coords to -120 deg
end