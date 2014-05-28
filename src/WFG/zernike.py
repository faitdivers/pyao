from scipy import *
import numpy
from math import *

from supportWFG import *

import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3

# Create a class to describe the wavefront
# TO DO: COMMENTS!!!!!! - Pydoc
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
        title = 'Phase \phi_{i}(x)of Zernike Polynomial: u = %d, v = %d' %(u,v)

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
        title = "Combined Phase, \phi(x), of the  Wavefront"
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
        num = ((-1)**s * gamma2(u - s))
        den = (gamma2(s) * gamma2(((u + v)/2.) - s) * gamma2(((u-v)/2.) - s))
        coor = rho**(u-(2*s))
        S = S + (num/den)*coor
        s += 1
    
    return scalar * S * pol
        
# Map i to (u,v) : u,v = zernikIndex(i)
# Maps an integer i to the zernike parameters (u,v) according to Noll's mapping
# The argument i must be integer and larger then 1. Other inputs may work,
# but are not guarenteed.
def zernikeIndex(i):
    u = 0
    iAux = i
    # First, create u by substracting the lowest possible i for the current u  
    while iAux > (u+1):
        u += 1
        iAux -= u        
    iAux -= 1
 
    # Determine if u is odd or even, for the correct range of possible v's and
    # select the v according to remainder of the u creation above   
    if (u % 2):
        V = range(1,u+1,2)
        #For debugging, uncomment below:
        #print V
        #print "u is odd, n = %d" %int(iAux/2.)
        v = V[int(iAux/2.)]
    else:
        V = range(0,u+1,2)
        #For debugging, uncomment below:
        #print V        
        #print "u is even, n = %f" %int(ceil(iAux/2.))
        v = V[int(ceil(iAux/2.))]
        
    # Map odd Noll indeces with a negative v    
    if (i % 2):
        v *= -1
        
    return u,v