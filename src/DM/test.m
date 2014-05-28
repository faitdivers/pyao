clc; clear all; close all;
x = 0:.1:10;
y = 0:.1:10;

    % parameters to characterize influence function
    w1= 2;
    w2= -1;
    sig1= 0.54;
    sig2= 0.85;
    mu = [3,5];
    for i = 1: length(x)
        for j = 1: length(y)
            S(i,j) = w1/(2*pi*sig1^2)*exp(-((x(i)-mu(1))^2+(y(j)-mu(2))^2)/(2*sig1^2))+...
                w2/(2*pi*sig2^2)*exp(-((x(i)-mu(1))^2+(y(j)-mu(2))^2)/(2*sig2^2));
%             plot3(x(i),y(i), S(i,j));
%             hold on;
        end
    end
    
    mu = [4.5,5];
    for i = 1: length(x)
        for j = 1: length(y)
            S2(i,j) = w1/(2*pi*sig1^2)*exp(-((x(i)-mu(1))^2+(y(j)-mu(2))^2)/(2*sig1^2))+...
                w2/(2*pi*sig2^2)*exp(-((x(i)-mu(1))^2+(y(j)-mu(2))^2)/(2*sig2^2));
%             plot3(x(i),y(i), S(i,j));
%             hold on;
        end
    end
    
%     x = repmat(x,length(x),1);
%     y = repmat(y',1,length(y'));
    x = repmat(x',1,length(x'));
    y = repmat(y,length(y),1);
    
    figure; surf(x,y,0.3*S+0.5*S2); hold on;
%     surf(x,y,0.5*S2); hold on;
    
    
            