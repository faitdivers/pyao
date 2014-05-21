from scipy import *
import numpy
from math import *
from nollMap import *
from supportWFG import *

import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3

#Create a class to house the wavefront
class ZernikeWave:
    def __init__(self):
        self.indices = [] #empty(0,numpy.uint32)
        self.weights = [] #empty(0)
    
    def addMode(self,i, alpha_i = 1):
        if not(isinstance(i,list)):
            i = [i]
        if not(isinstance(alpha_i,list)):
            alpha_i = [alpha_i]
        if len(i) != len(alpha_i):
            print("ERROR: Indices list and weighting list must have equal lengths.")
            return   
            
        loc = 0
        for n in i:
            if not(self.modeExists(n)):
                self.indices.append(n)
                self.weights.append(alpha_i[loc])
            else:
                print('WARNING: Mode %d is already existant, mode changed.' %n)
                self.changeModeWeight(n,alpha_i[loc])
            loc += 1
            
    def changeModeWeight(self,iModeToChange,alpha_i = 1):
        if not(isinstance(iModeToChange,list)):
            iModeToChange = [iModeToChange]
        if not(isinstance(alpha_i,list)):
            alpha_i = [alpha_i]
        if len(iModeToChange) != len(alpha_i):
            print("ERROR: Indices list and weighting list must have equal lengths.")
            return   
            
        loc = 0
        for n in iModeToChange:
            if self.modeExists(n):
                self.weights[self.indices.index(n)] = alpha_i[loc]
            else:
                print('WARNING: Mode %d non-existant, mode appended.' %n)
                self.addMode(n,alpha_i[loc])
            loc += 1
    
    def removeMode(self,iToRemove):
        if not(isinstance(iToRemove,list)):
            iToRemove = [iToRemove];

        loc = 0
        for n in iToRemove:
            if self.modeExists(n):          
                self.weights.remove(self.weights[self.indices.index(n)])
                self.indices.remove(n)
            else:
                print("WARNING: Mode %d not present in the wavefront." %n)
            loc += 1
               
    def modeExists(self,i):
        return (self.indices.count(i) > 0)
    
    def getModes(self):
        return self.indices
        
    def getWeights(self):
        return self.weights
    
    def createWavefront(self,nX,nY):
        numberOfModes = len(self.indices)
        pos = 0

        WF = zeros([nX,nY])
        X,Y = createGrid(nX,nY)
        R,T = cart2pol(X,Y)
        aperture = circ(X,Y)
        
        while pos < numberOfModes:
            mode = self.indices[pos]
            weight = self.weights[pos]
            zi = zernike(R,T,mode)*aperture
            WF += weight * zi
            pos += 1

        return WF
    
    def decomposeWavefront(self,W):
        numberOfModes = len(self.indices)
        pos = 0
        
        nX = int(size(W,0))
        nY = int(size(W,0))
        
        W = zeros([nX,nY])
        X,Y = createGrid(nX,nY)
        R,T = cart2pol(X,Y)
        aperture = circ(X,Y)
        indx = array(aperture,'bool')
        
        while pos < numberOfModes:
            mode = self.indices[pos]
            weight = self.weights[pos]
            zi = zernike(R,T,mode)*aperture
            W += weight * zi
            if pos == 0:                
                zi = zi[indx]
                Z = reshape(zi,(len(zi),1))
            else:
                zi = zi[indx]
                zi = reshape(zi,(len(zi),1))
                Z = numpy.concatenate((Z,zi),1) 
            pos += 1
            
        W = W[indx]
        A = numpy.dot(numpy.linalg.pinv(Z),W)
        A = numpy.reshape(A,(len(A),1))
        return Z,A
            
    def plotMode(self,iToPlot,nX,nY):
        if self.modeExists(iToPlot):
            alpha = self.weights[self.indices.index(iToPlot)]
        else:
            print("WARNING: Mode %d does not exist, plotting default mode." %iToPlot)
            alpha = 1.0
            
        u,v = zernikeIndex(iToPlot)
        X,Y = createGrid(nX,nY)
        R,T = cart2pol(X,Y)
        Zg = alpha*zernike(R,T,u,v)*circ(X,Y)
        title = 'Zernike Polynomial: u = %d, v = %d' %(u,v)

        # Plot results in a surface plot
        fig = p.figure();
        ax = p3.Axes3D(fig)
        ax.plot_surface(X,Y,Zg, rstride=1, cstride=1, cmap='jet')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel(title)
        p.show()
    
    def plotWavefront(self,nX,nY):
        X,Y = createGrid(nX,nY)
        WF = self.createWavefront(nX,nY)  
        print WF
        title = "Combined Wavefront"
        # Plot results in a surface plot
        fig = p.figure();
        ax = p3.Axes3D(fig)
        ax.plot_surface(X,Y,WF, rstride=1, cstride=1, cmap='jet')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel(title)
        p.show()
        
        
    
       

# Create Zernike Grid : Z_{u}^{v} = zernike(rho,theta,n)
# Compute the zernike mode based on Noll's index n, at the specified location
# given by rho and theta. Accepts an ARRAY of locations rho and theta as well as 
# scalar values.
# Create Zernike Grid : Z_{u}^{v} = zernike(rho,theta,u,v)
# Compute the zernike mode based on the indices (u,v) at the specified location
# given by rho and theta. Accepts an ARRAY of locations rho and theta as well as 
# scalar values.

# SUGGESTIONS: Adjust code to accept a range of n's or (u,v)'s  and return a
# collection of the corresponding modes.
def zernike(rho,theta,u,v = None):
    if v is None:
        u,v = zernikeIndex(u)
    elif (u < 0):
        #Return invalid index selection to the user.
        #TO DO: Throw an error here?
        print("ERROR: u or i must be positive!")
        return        
            
    # The scaler of the part of the Zernike function, or not s dependant
    scalar = sqrt((2 * (u + 1)) / (1 + kroneckerDelta(v) ))
    # Determine of the (u,v)-combination is even or odd
    isOdd = ((u > 0) & (v > 0)) | ((v == 0) & (mod(u+2,4) == 0))

    # Now apply the even or odd scaler
    # TO DO: Merge condition into the if - statement 
    if isOdd:
        pol = numpy.cos(v*theta)
    else:
        pol = numpy.sin(v*theta)
    
    # Store the intermediate result of the summation in S, iterate with s
    S = 0
    s = 0
    while s <= 0.5 * (u - v):
        num = ((-1)**s * gamma(u - s))
        den = (gamma(s) * gamma(((u + v)/2.) - s) * gamma(((u-v)/2.) - s))
        coor = rho**(u-(2*s))
        S = S + (num/den)*coor
        s += 1
    
    return scalar * S * pol
        
