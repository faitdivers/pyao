from numpy import *
import numpy
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

def dm(actCom, paramsSens, paramsAct):

    noApertx= paramsSens['noApertx'];
    noAperty= paramsSens['noAperty'];
    numImagx= paramsSens['numImagx'];
    numImagy= paramsSens['numImagy'];
    numPupilx=paramsSens['numPupilx'];
    numPupily=paramsSens['numPupily'];		
    numActx=noApertx;      
    numActy=noAperty;
    
    noApert = noApertx*noAperty; # number of subapertures
     
    numAct = numActx*numActy; # number of actuators  
    
    # length of wavefront reconstruction vector
    nwfRec = (noApertx+1)*(noAperty+1);
    
    
    d = 10.0*power(10.0,-6);  # spacing between actuators [m]
    subAperture = d; # radius of subaperture is assumed to be equal to d
    
    # parameters to characterize influence function
    w1= 2;
    w2= -1;
    sig1= 0.54*subAperture;
    sig2= 0.85*subAperture;
    
    #calculate the position of the actuators
    posAct = numpy.zeros([numActx*numActy,2]);
    x = linspace(d,(noApertx)*d,noApertx);  # discretize the square
    y = linspace(d,(noAperty)*d,noAperty);
    for i in range (0, numActx):
        for j in range (0,numActy):
            posAct[i*numActx+j][0] = x[i];
            posAct[i*numActy+j][1] = y[j];
    
    pl.plot(posAct[:,0], posAct[:,1], '+');
    pl.axis([0, x.max()+d, 0, y.max()+d]);
    
    # calculate the position of the wavefronts
    posWr = numpy.zeros([(numActx+2)*(numActy+2),2]);
    max_X = (noApertx+1)*d;
    dwf = max_X/(noApertx+3); # wavefront spacing
    xwr = linspace(dwf,(noApertx+2)*dwf,noApertx+2);
    ywr = linspace(dwf,(noAperty+2)*dwf,noApertx+2);    
    for i in range (0, xwr.size):
        for j in range (0, ywr.size):
            posWr[i*xwr.size+j][0] = xwr[i];
            posWr[i*ywr.size+j][1] = ywr[j];
    
    # hold on;
    pl.plot(posWr[:,0], posWr[:,1], 'r+');
    pl.axis([0, x.max()+d, 0, y.max()+d]);
    
    # length of wavefront reconstruction vector
    nwfRec = xwr.size*ywr.size;    
    
    u = ones([numAct, 1]);
    
    # calculate influence matrix H
    H = zeros([nwfRec,numAct]);
    for i in range (0, nwfRec):
        for j in range ( 0, numAct):
            H[i][j] = w1/(2*pi*power(sig1,2))*exp(-(power((posWr[i][0]-posAct[j][0]),2)+ power((posWr[i][1]- posAct[j][1]),2))/(2*power(sig1,2)))+ w2/(2*pi*power(sig2,2))*exp(-(power((posWr[i][0]-posAct[j][0]),2)+power((posWr[i][1]-posAct[j][1]),2))/(2*power(sig2,2)));            
            
    wfRec = 0.5+0.01*random.randn(nwfRec,1); # dummy wavefront reconstruction vector
    
    # least square solution
    u = dot(dot(numpy.linalg.inv(dot(H.T,H)),H.T),wfRec);
    # u = pinv(H)*wfRec; # alternatives for pseudo inverse
    
    # residual error
    wres = wfRec - dot(H,u);
    
    # plot the deformable mirror (after wave front reconstruction)
    xgrid = linspace(0,(noApertx)*d,101);
    ygrid = linspace(0,(noAperty)*d,101); 
    X, Y = numpy.meshgrid(xgrid, ygrid)
    #xgridt = xgrid.T;
    #xgrids = tile(xgridt,[1,xgrid.T.size]);
    #ygrids = tile(ygrid,[ygrid.size,1]);
    
    S = zeros([numAct+1, numAct+1]);
    for i in range(0,xgrid.size):
        for j in range(0,ygrid.size):
            sum = 0;
            for k in range(0, numAct):
                Sval = (w1/(2*pi*power(sig1,2))*exp(-(power((xgrid[i]-posAct[k][0]),2)+ power((xgrid[i]-posAct[k][0]),2))/(2*power(sig1,2)))+ w2/(2*pi*power(sig2,2))*exp(-(power((xgrid[i]-posAct[k][0]),2)+power((ygrid[j]- posAct[k][1]),2))/(2*power(sig2,2))))*u[k];      					
                sum = sum + Sval;
                S[i,j] = sum;
    fig = pl.figure();
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, S);#, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)			
    return zeros((paramsSens['numPupilx'],paramsSens['numPupily']))

