
function ordered  = primsAlg(points)
% This function takes a 1xN array of points in the form [x1 y1 z1 x2 y2 z2] 
% returns the same array of points reordered to the optimal path
    disp(points);
    points = transpose(points);
    points = points(:);
    points = transpose(points);
    
    % Step 1: Calculate the distances between the points
    % This can either be done with padding points so diagonal distances along
    % three dimensions are not used or with only the original points.

    % For this project we have chosen to pad the points which means we can
    % ignore the z aspect of our distances (our distances will become the
    % weight of that edge connection between the vertices/points)

    % Start with an original point (does not matter which)
    ordered = [points(1,1) points(1,2) points(1,3)];
    % Take the point out of the points array
    points(1:3) = [];
    
    % Take the size of both the ordered vertices
    [o,p] = size(ordered);
    
    
    while 1~=0
        [m,n] = size(points);
        [o,p] = size(ordered);
        istore = 0;
        % Just throw minDist as something large that would never be reached
        % initially
        minDist = 10000;
        % Extract the x and y co-ordinates
        x1 = ordered(o,1);
        y1 = ordered(o,2);
        
        i = 1;
        while i<=n
            x2 = points(1,i);
            y2 = points(1,i+1);
            dist = sqrt((x2-x1)^2 + (y2-y1)^2);
            if dist<minDist
                minDist = dist;
                xf = x2;
                yf = y2;
                zf = points(1,i+2);
                istore = i;
            end
            i=i+3;
        end
        add = [xf yf zf];
        % Add vertex to final vertices
        ordered = [ordered;add];
        % Take vertex out of original point array
        if istore==1 
            points(1:3) = [];
        elseif istore==n-2
            points(n-2:n) = [];
        else
            points(istore:istore+2) = [];
        end
            % Retake the new sizes of both of the arrays
            [o,p] = size(ordered);
            [m,n] = size(points);
   
        
        % If we have all the points already, (and therefore points is empty) quit the while loop
        if n==0
            break
        end
    end
end