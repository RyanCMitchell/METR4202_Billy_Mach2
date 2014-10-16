function [billypoints] = points2billycoords(givenpoints)
    %this function converts the output of Lab1RandLocations to usable
    %Billy coordinates
    l1 = size(givenpoints);
    l2 = l1(1);
    for j=1:l2
        givenpoints(j,1) = -32*(givenpoints(j,1)-5.5);
        givenpoints(j,2) = 32*(givenpoints(j,2)-3.5);
        givenpoints(j,3) = 19.2*(givenpoints(j,3));
    end
    billypoints = givenpoints;
end