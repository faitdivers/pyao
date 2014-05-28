% function wfDM = mainDM(wfRec, actCommands, paramsSensor)
    clear all; clc; close all;
    format long;    
    
    numPupilx= 100;
    numPupily= 100;
 
    numImagx= 100;
    numImagy= 100;
 
    noApertx= 10;
    noAperty= 10;
    noApert = noApertx*noAperty;
    
    % paramsActuator 
    % number of actuators
    numActx= 10;
    numActy= 10;
    numAct = numActx*numActy;
    
    % calculate the position of the actuators    
    d = 10*10^(-6); % spacing between actuators [m]
    subAperture = d;
    
    % parameters to characterize influence function
    w1= 2;
    w2= -1;
    sig1= 0.54*subAperture;
    sig2= 0.85*subAperture;
    
    x = transpose(d:d:(noApertx)*d);
    y = transpose(d:d:(noAperty)*d);
    for i = 1: numActx 
        for j = 1: numActy 
            posAct((i-1)*numActx+j,1) = x(i);
            posAct((i-1)*numActy+j,2) = y(j);
        end
    end
    plot(posAct(:,1), posAct(:,2), '+');
    axis([0 max(x)+d 0 max(y)+d]);
    
    % calculate the position of the wavefronts
    max_X = (noApertx+1)*d;
    dwf = max_X/(noApertx+3);
    xwr = transpose(dwf:dwf:(noApertx+2)*dwf);
    ywr = transpose(dwf:dwf:(noAperty+2)*dwf);    
    for i = 1: length(xwr)
        for j = 1: length(ywr)
            posWr((i-1)*length(xwr)+j,1) = xwr(i);
            posWr((i-1)*length(ywr)+j,2) = ywr(j);
        end
    end
    hold on;
    plot(posWr(:,1), posWr(:,2), 'r+');
    axis([0 max(x)+d 0 max(y)+d]);    
    

    % length of wavefront reconstruction vector
    nwfRec = (length(xwr))*(length(ywr));    
    
    u = ones(numAct, 1);
        
    % calculate influence matrix H
    for i = 1: nwfRec
        for j = 1: numAct
            H(i,j) = w1/(2*pi*sig1^2)*exp(-((posWr(i,1)-posAct(j,1))^2+ ...
                (posWr(i,2)- posAct(j,2))^2)/(2*sig1^2))+ w2/(2*pi*sig2^2)...
                *exp(-((posWr(i,1)-posAct(j,1))^2+(posWr(i,2)- ...
                posAct(j,2))^2)/(2*sig2^2));            
        end
    end
    
    wfRec = 0.5+0.01*randn(nwfRec,1); % dummy wavefront reconstruction vector
    
    % least square solution
    u = inv(transpose(H)*H)*transpose(H)*wfRec;
%     u = pinv(H)*wfRec;
    
    % residual error
    wres = wfRec - H*u;
    
    % plot the deformable mirror (after wave front reconstruction)
    xgrid = 0:d/10:(noApertx+1)*d;
    ygrid = 0:d/10:(noAperty+1)*d; 
%     xgrids = repmat(xgrid',1,length(xgrid'));
%     ygrids = repmat(ygrid,length(ygrid),1);
    xgrids = repmat(xgrid,length(xgrid),1);
    ygrids = repmat(ygrid,length(ygrid),1);    
%     figure;
% for k = 1: numAct                
    for i = 1:length(xgrid)
        for j = 1: length(ygrid)
            sum = 0;
            for k = 1: numAct                
                Sval = (w1/(2*pi*sig1^2)*exp(-((xgrid(i)-posAct(k,1))^2+ ...
                (ygrid(j)- posAct(k,2))^2)/(2*sig1^2))+ w2/(2*pi*sig2^2)...
                *exp(-((xgrid(i)-posAct(k,1))^2+(ygrid(j)- ...
                posAct(k,2))^2)/(2*sig2^2)))*u(k);  
                sum = sum + Sval;                
                S(i,j) = sum;
            end
        end
    end
%     surf(xgrids, ygrids, S );%- 87.13140);
    [X, Y] = meshgrid(xgrid, ygrid);
    figure; surf(X', Y', S );
    hold on; 
% end
%     xgrid = repmat(xgrid',1,length(xgrid'));
%     ygrid = repmat(ygrid,length(ygrid),1);
%     figure; surf(xgrid, ygrid, S );%- 87.13140);
%     surf(repmat(posApert(:,1),noApert,1), repmat(posAct(:,2), 1, numAct), H)

    

