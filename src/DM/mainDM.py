from numpy import *
import numpy
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def calculateH(posWfr, posAct, paramsAct):
    numActx = paramsAct['numActx']
    numActy = paramsAct['numActy']
    sig1 = paramsAct['sig1']
    sig2 = paramsAct['sig2']
    w1 = paramsAct['w1']
    w2 = paramsAct['w2']
    nwfRec = (numActx+1)*(numActy+1)
    numAct = numActx*numActy
    
    H = zeros([nwfRec,numAct]);
    for i in range (0, nwfRec):
        for j in range ( 0, numAct):
            H[i][j] = w1/(2*pi*sig1**2)*exp(-((posWfr[i][0]-posAct[j][0])**2+
            (posWfr[i][1]- posAct[j][1])**2)/(2*sig1**2))+ w2/(2*pi*sig2**2)*exp(-
            ((posWfr[i][0]-posAct[j][0])**2+(posWfr[i][1]-posAct[j][1])**2)/(2*sig2**2))
    return H

    
def plotWFR(wfr, noApertx, noAperty):
    # plot a wavefront
    W = wfr.reshape(noAperty+1, noApertx+1)
    xgridw = linspace(0,1,noApertx+1)
    ygridw = linspace(0,1,noAperty+1)        
    Xw, Yw = numpy.meshgrid(xgridw, ygridw)
    figu = pl.figure()
    axi = figu.gca(projection='3d')        
    surfa = axi.plot_surface(Xw, Yw, W, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=True)        
    figu.colorbar(surfa, shrink=0.5, aspect=5)
    axi.set_xlim3d(0, xgridw.max())
    axi.set_ylim3d(0, ygridw.max())
    axi.set_zlim3d(W.min(), 1.03*W.max())
    pl.show()
    
def calculatePosWFr(paramsAct, paramsSens, dact):
    lensCentx = paramsSens['lensCentx']
    lensCenty = paramsSens['lensCenty']      
    noApertx= paramsSens['noApertx']
    noAperty= paramsSens['noAperty']
    
    # calculate the position of the wavefronts according to hudgin geometry
    nWrx = noApertx+1
    nWry = noAperty+1    
    posWfr = numpy.zeros([nWrx*nWry,2])
    
    lensCentPos = 0;
    upperflag = 0;
    for i in range(0, nWry):
        for j in range (0, nWrx):        
            if (i*nWrx+j<(i+1)*nWrx-1):
                posWfr[i*nWrx+j][0] = lensCentx[lensCentPos] - dact/2
                posWfr[i*nWrx+j][1] = lensCenty[lensCentPos] - dact/2                                
            else:
                posWfr[i*nWrx+j][0] = lensCentx[lensCentPos] + dact/2
                posWfr[i*nWrx+j][1] = lensCenty[lensCentPos] - dact/2                                                
                    
            if (j<noApertx-1)&(i<nWry-1)&((i*nWrx+j)<(nWrx*(nWry-1)-1)):             
                lensCentPos = lensCentPos + 1
            if upperflag == 1:                
                posWfr[i*nWrx+j][0] = posWfr[(i-1)*nWrx+j][0]
                posWfr[i*nWrx+j][1] = posWfr[(i-1)*nWrx+j][1] + dact
#        print ("limit:",(i+1)*nWrx-1)
        if ((i*nWrx+j)==((i+1)*nWrx-1))&((i*nWrx+j)<(nWrx*(nWry-1)-1)):
            lensCentPos = lensCentPos + 1 
        if ((i*nWrx+j)>=(nWrx*(nWry-1)-1)):
            upperflag = 1;            

    return posWfr
    
def dmOptimizer(paramsSens, paramsAct):
    noApertx= paramsSens['noApertx']
    noAperty= paramsSens['noAperty']
    lensCentx = paramsSens['lensCentx']
    lensCenty = paramsSens['lensCenty']    
    numActx=paramsAct['numActx']
    numActy=paramsAct['numActy']
    dl = lensCentx[1] - lensCentx[0] # distance of two lenslet
     
    numAct = numActx*numActy # number of actuators  
    
    # length of wavefront reconstruction vector
    nwfRec = (noApertx+1)*(noAperty+1)
        
    wfRec = 0.5+0.001*random.randn(nwfRec,1) # generate wavefront reconstruction vector
        
    # parameters to characterize influence function
    w1= 2
    w2= -1
    sig1= 0.54*dl
    sig2= 0.85*dl
    
        
    posWfr = calculatePosWFr(numActx, numActy, noApertx, noAperty, lensCentx, lensCenty, dl)
    
    #calculate the position of the actuators
    posAct = numpy.zeros([numActx*numActy,2])
    posAct = array([lensCentx, lensCenty])
    posAct = posAct.T 
    
    u = ones([numAct, 1])
    
    # calculate influence matrix H
    H = calculateH(nwfRec, numAct, posWfr, posAct, sig1, sig2, w1, w2) 
    
    # least square solution
    u = dot(numpy.linalg.pinv(H),wfRec) # alternatives for pseudo inverse
    return u
            
def dm(actCommand, paramsAct):
    H = paramsAct['H']
    # residual error
    wfDM = dot(H,actCommand)
#    wfRes = wfRec - wfDM
#    powerRes = sqrt((wfRes*wfRes).mean())

    
    return wfDM
    
    #return zeros((paramsSens['numPupilx'],paramsSens['numPupily']))

