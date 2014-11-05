rf = 191; %142.5 bicep length
re = 213; %154.4 forarm length 
f = 154.4*2; %280.51 top sidelength 
e = 32.5*2; %93.53 base sidelength
t = (f - e)*tand(30)/2;


Rb = [cosd(120) -sind(120); sind(120) cosd(120)];
Ra = [cosd(-120) -sind(-120); sind(-120) cosd(-120)];
Pc = [f/(4*cosd(30));0];
Pb = Rb*Pc;
Pa = Ra*Pc;