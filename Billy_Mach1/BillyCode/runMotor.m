function runMotor(degrees, h,intendedpos,correct)
    
    degx = degrees(1,1);
    degy = degrees(1,2);
    degz = degrees(1,3);
    
    %disp(degx/5);
    %disp(degy/5);
    %disp(degz/5);
    disp([degx/5 degy/5 degz/5]);
    
    degxtemp = int16(degx);
    degytemp = int16(degy);
    degztemp = int16(degz);
    % Undo negatives and assign them to speeds
    [degx,degy,degz,speed1,speed2,speed3] = swappitySwap([degx degy degz]);
    
    
    % Break if there are any imaginary components (and therefore is not a
    % valid move to position to
    if (~isreal(degx))||(~isreal(degy))||(~isreal(degz))
        error('One of the moves is not valid');
    end
    
    
    
    %disp(degy/5);
    %disp(degz/5);
    
    
    
    % Round the numbers to only input integers to NXC_MotorControl as
    % required
    %degx = uint16(abs(degx));
    %degy = uint16(abs(degy));
    %degz = uint16(abs(degz));
    
    if degx < 1
        degx = 1;
    end
    if degy < 1
        degy = 1;
    end
    if degz < 1
        degz = 1;
    end
        
    %disp(degx/5);
    %disp(degy/5);
    %disp(degz/5);
    
    %str = input('Do you want to run with these angles?','s');
    
    %if strcmp(str,'y')
    if strcmp('yes','yes')
        mA = NXTMotor('A','Power',speed1,'TachoLimit',degx,'ActionAtTachoLimit','HoldBrake','SpeedRegulation',true,'SmoothStart',false);
        mB = NXTMotor('B','Power',speed2,'TachoLimit',degy,'ActionAtTachoLimit','HoldBrake','SpeedRegulation',true,'SmoothStart',false);
        mC = NXTMotor('C','Power',speed3,'TachoLimit',degz,'ActionAtTachoLimit','HoldBrake','SpeedRegulation',true,'SmoothStart',false);
        mA.SendToNXT();
        mB.SendToNXT();
        mC.SendToNXT();
        mA.WaitFor(2);
        mB.WaitFor(2);
        mC.WaitFor(2);
        %disp('currentpos');
        [posx posy posz] = getRTC(h);
        %disp([posx posy posz]);
        %disp([degxtemp degytemp degztemp]);
        
        
        if(((abs(posx - intendedpos(1,1)) > 1)||(abs(posy - intendedpos(1,2)) > 1)||(abs(posy - intendedpos(1,3)) > 1))&&(correct > 0))
            %disp('inaccuratestatement');
            [degx2,degy2,degz2,speed1,speed2,speed3] = swappitySwap([(posx - intendedpos(1,1)) (posy - intendedpos(1,2)) (posz - intendedpos(1,3))]);
            mA.TachoLimit = degx2;
            mB.TachoLimit = degy2;
            mC.TachoLimit = degz2;
            mA.Power = -speed1;
            mB.Power = -speed2;
            mC.Power = -speed3;
            if degx2 ~= 0
                mA.SendToNXT();
                %disp('mA adjusted');
            end
            if degy2 ~= 0
                mB.SendToNXT();
                %disp('mB adjusted');
            end
            if degz2 ~= 0
                mC.SendToNXT();
                %disp('mC adjusted');
            end
            mA.WaitFor(1);
            mB.WaitFor(1);
            mC.WaitFor(1);
            [posx posy posz] = getRTC(h);
            disp('Corrected position:')
            disp([posx posy posz]);
            %disp([posx posy posz]);
%             if(correct == 2)
%                 disp('inaccuratestatement2');
%                 [degx2,degy2,degz2,speed1,speed2,speed3] = swappitySwap([(posx - intendedpos(1,1)) (posy - intendedpos(1,2)) (posz - intendedpos(1,3))]);
%                 mA.TachoLimit = degx2;
%                 mB.TachoLimit = degy2;
%                 mC.TachoLimit = degz2;
%                 mA.Power = -speed1;
%                 mB.Power = -speed2;
%                 mC.Power = -speed3;
%                 if degx2 ~= 0
%                     mA.SendToNXT();
%                     disp('mA adjusted2');
%                 end
%                 if degy2 ~= 0
%                     mB.SendToNXT();
%                     disp('mB adjusted2');
%                 end
%                 if degz2 ~= 0
%                     mC.SendToNXT();
%                     disp('mC adjusted2');
%                 end
%                 mA.WaitFor(1);
%                 mB.WaitFor(1);
%                 mC.WaitFor(1);
%                 [posx posy posz] = getRTC(h);
%                 disp([posx posy posz]);
%             end
        end
        % Run all three motors to each degree
        %NXC_MotorControl(0,speed1,degx, false,'Brake',true);
        %NXC_MotorControl(1,speed2,degy, false,'Brake',true);
        %NXC_MotorControl(2,speed3,degz, false,'Brake',true);
        
        
        
    else
        return
    end
end

