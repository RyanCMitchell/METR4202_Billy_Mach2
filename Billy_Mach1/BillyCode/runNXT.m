function runNXT (points,numtimes)
    % Beginning point is to get a reference from the starting point as all
    % encoders default to 0 when the NXT is turned on
    beginz = -336; %-320;
    % Reorder points via calculation of shortest path at each step. This is
    % essentially djikstra's algorithm in this case because we have every
    % point fully connected to every other point (there is no limit to
    % where we can move from one to another). Because of this, Prim's
    % algorithm also has no computational benefit over djikstra's
    %points = [[5.5,3.5,6];points];
    newpoints1 = primsAlg(points);
    newpoints = newpoints1;
    for i=1:numtimes-1
        newpoints = [newpoints;newpoints1];
    end
    newpoints = points2billycoords(newpoints);
    newpoints = [newpoints;[0 0 115];[0 0 125]];
    %disp(newpoints);
    %newpoints = points;
    [m,n] = size(newpoints);
    newpoints2 = [];
    for i=1:m
        
        y = newpoints(i,:);
        y(1,3) = y(1,3)+50;
        if y(1,3) > 125
            y(1,3) = 125;
        end
        newpoints2 = [newpoints2;y];
        newpoints2 = [newpoints2;newpoints(i,:)];
        newpoints2 = [newpoints2;y];
        
    end
    %newpoints2(1,:) = [];
    %newpoints2(1,:) = [];
    [p,q] = size(newpoints2);
    newpoints2(p,:) = [];
    newpoints2(p-2,:) = [];
    newpoints = newpoints2;
    
    disp(newpoints);
    
    % Connect to NXT and grab the handle
    h =  COM_OpenNXT();
    COM_SetDefaultNXT(h);
    
    % Reset the rotationCounter on the motors
    %NXT_ResetMotorPosition(0, false, h);
    %NXT_ResetMotorPosition(1, false, h);
    %NXT_ResetMotorPosition(2, false, h);


    [m,n] = size(newpoints);
    % Assuming inputs are 1-row arrays of subsequent x,y and z co-ords
    j = 1;
    temp = 3;
    while j<=m
        % Extract each points co-ordinates from the input
        x = newpoints(j,1);
        y = newpoints(j,2);
        z = newpoints(j,3);
        disp('Point we are going to:');
        disp([x y z]);
        %if x > 0
        %    x = x + x*(17/160);
        %else
        %    x = x+x*(25/160);
        %end
        %y = y+y*(7/96);
        %if y > 0
        %    
        %    y = y + 6.1613*(1.0082^x);
        %else
        %    y = y - 6.1613*(1.0082^x);
        %end    
        
        
        y = y - (-0.009375*y + 0.25)*6.979*(1.0093^x);
        
        if x > 0
            x = x + 3 + 3*(x)/80;
        elseif 0 > x > -32
            if y < -32
                x = x - ((y/80)*12 + 4);
            end
        elseif x < -32;
            x = x + (x + 32)*(6/32);
        end
        %if((x > 0)&&(y<0))
        %    z = z + 10;
        %end
        z = z - 10;
        
        % Run the inverse kinematics for the position of each motor (in
        % degrees)
        %degx = inverseKin(x,y,z+beginz,0);
        %degy = inverseKin(x,y,z+beginz,120);
        %degz = inverseKin(x,y,z+beginz,-120);
        R = [1 1; 1 1];
        R = [cos(0.475) -sin(0.475); sin(0.475) cos(0.475)];
        X = [x;y];
        X = R * X;
        %X = X.*(96/(96-12));
        
        [ang1 ang2 ang3] = delta_calcInverse(X(1,1),X(2,1),z+beginz);
        %intendedpos = [ang1 ang2 ang3];
        %disp(intendedpos);
        %intendedpos = -[(ang1-60.8664)*5 (ang2-60.8664)*5 (ang3-60.8664)*5]; % *5 to account for gearing down
        angle = 38.5844;
        intendedpos = -[(ang1-angle)*5 (ang2-angle)*5 (ang3-angle)*5];
        
        % Pass handle to get the current rotation counters of each motor in
        % a 1x3 array
        w1 = NXT_GetOutputState(0,h);
        w2 = NXT_GetOutputState(1,h);
        w3 = NXT_GetOutputState(2,h);
        r1 = w1.RotationCount;
        r2 = w2.RotationCount;
        r3 = w3.RotationCount;
        
        currentpos = [r1 r2 r3];
        %[currentpos(1), currentpos(2), currentpos(3)] = getRTC(h);
        
        %disp('intendedpos');
        %disp(intendedpos);
        
        % Minus currentpos from intended pos to get the relative movement
        % required
        moveangles = intendedpos - currentpos;
                
        % Run the movement
        if temp == 3
            runMotor(moveangles,h,intendedpos,1);
            temp = 1;
        else
            runMotor(moveangles,h,intendedpos,0);
            temp = temp + 1;
        end
        
        %if (z == 115)
        %     disp('Correction 2');
        %     runMotor(moveangles,h,intendedpos,2);
        %end
        %w1 = NXT_GetOutputState(0,h);
        %w2 = NXT_GetOutputState(1,h);
        %w3 = NXT_GetOutputState(2,h);
        %r1 = w1.RotationCount;
        %r2 = w2.RotationCount;
        %r3 = w3.RotationCount;

        %disp([r1, r2, r3]);
        
        j= j+1;
    end
    
    
end