function theta = inverseKin (X, Y, Z, motorpos)

theta = 0;

if (motorpos == 0)
    Cx=X;
    Cy=Y;
elseif (motorpos == 120)
    Cx = X*cosd(120) + Y*sind(120);
    Cy = -X*sind(120) + Y*cosd(120);
elseif (motorpos == -120)
    Cx = X*cosd(120) - Y*sind(120);
    Cy = X*sind(120) + Y*cosd(120);
end
    
    

% Load the parameters from the parameter file
parameters;

L3 = sqrt(L2^2 - Cx^2);


Ay = -Ra;
PCy= Cy - Rb;
dn = (L1 + sqrt(L2^2 - (Ay - PCy)^2));

if (abs(Z) <= dn)
    a = (4*Z^2 + (2*Ay - 2*PCy)^2);
    b = ( -8*Ay * Z^2 + (4*Ay - 4*PCy)*(L1^2 - L3^2 - Ay^2 + PCy^2 + Z^2));
    c = (4*Ay^2 * Z^2 - (4*Z^2) * (L1^2) + (L1^2 - L3^2 - Ay^2 + PCy^2 + Z^2)^2);
    
    D = sqrt(b^2 - 4*a*c);
    By1 = ( -b - D)/(2*a);
    By2 = ( -b + D)/(2*a);
    
    if abs(By1)>abs(By2)
        Bz1 = (By1*(2*Ay - 2*PCy) + L1^2 - L3^2 - Ay^2 + PCy^2 + Z^2)/(2*Z);
        theta = atan(Bz1/(Ay - By1))*(180/pi);
    else
        Bz1 = (By2*(2*Ay - 2*PCy) + L1^2 - L3^2 - Ay^2 + PCy^2 + Z^2)/(2*Z);
        theta = atan(Bz1/(Ay - By2))*(180/pi);
    end
else
    % Send an error
    return
end
