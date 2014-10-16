function doa3dmodel()
    goodpointsx = [];
    goodpointsy = [];
    goodpointsz = [];
    for i=-96:3:96
        disp(i);
        for j=-160:3:160
            for k=-360:3:-50
                [theta1 theta2 theta3] = delta_calcInverse(i,j,k);
                if((theta1 == false)||(theta2 == false)||(theta3==false))
                    
                else
                    goodpointsx = [goodpointsx;i];
                    goodpointsy = [goodpointsy;j];
                    goodpointsz = [goodpointsz;k];
                
                end
            end
        end
    end
    figure
    scatter3(goodpointsx,goodpointsy,goodpointsz);
end
