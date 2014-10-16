rf = 184;%142.5;
re = 232; %154.4
f = 154.4*2; %280.51;
e = 46.3*2; %93.53;
t = (f - e)*tand(30)/2;


Rb = [cosd(120) -sind(120); sind(120) cosd(120)];
Ra = [cosd(-120) -sind(-120); sind(-120) cosd(-120)];
Pc = [f/(4*cosd(30));0];
Pb = Rb*Pc;
Pa = Ra*Pc;