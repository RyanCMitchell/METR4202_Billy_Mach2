rf = 184;%142.5;
re = 232; %154.4
h = 336;

breakpoints = [];
possiblepoints
l1 = size(possiblepoints2);
l2 = l1(1);
for j=1:l2
    a = possiblepoints2(j,:);
    x0 = a(1);
    y0 = a(2);
    z0 = a(3);
    [theta1, theta2, theta3] = delta_calcInverse_design(x0, y0, z0, rf, re, h);
    disp([x0 y0 z0])
    disp([theta1, theta2, theta3])
    if isnan(theta1)
       breakpoints = [breakpoints; [x0 y0 z0]];
    end
end