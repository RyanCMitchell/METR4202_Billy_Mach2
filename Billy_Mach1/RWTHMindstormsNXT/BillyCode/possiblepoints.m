possiblepoints1 = [];
for i=1:10
    for j=1:6
        for k=1:5
            possiblepoints1 = [possiblepoints1; [i j k]];
        end
    end
end         
possiblepoints2 = points2billycoords(possiblepoints1);