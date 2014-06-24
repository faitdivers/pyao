from scipy import *
import numpy
import numpy as np
from math import *

def kroneckerDelta(x):
    if x == 0:
        return 1.
    else:
        return 0.

# Factorial function : gamma(n) = n!
# Recall: Gamma(n+1) = n!, currently a lazy implementation, without the need
# to add 1 to the argument. The function does NOT solve int_{0}^{inf} = t^{n-1}*e^{-t} dt.
# It only extends validity beyond n < 0. The result is only guaranteed for integer 
# arguments.
def gamma2(n):
    f = 1
    if n >=0:
        while n > 1:
            f = f * n
            n -= 1
        return f
    else:
        return inf  
    #if n > 0:
    #    return math.gamma(n + 1)
    #else:
    #    return inf
  
# Map Cartesian coordinates of polar coordinates : (r,t) = mapping(x,y)
# Computes the radius R and angle THETA from the (arrays) X and Y, representing
# the Cartesian coordinates. The index in the arrays couples the information in X and Y.      
def cart2pol(X,Y):
    R = numpy.sqrt(X*X + Y*Y)
    THETA = arctan2(Y,X)
    return R,THETA

# Map Cartesian coordinates of polar coordinates : (x,t) = mapping(r,t)
# Computes the X location and Y location from the (arrays) R and THETA, representing
# the polar coordinates. The index in the arrays couples the information in R and THETA.      
def pol2cart(R,THETA):
    X = R*cos(THETA)
    Y = R*sin(THETA)
    return X, Y
 
# Create a meshgrid, with a specified number of elements in both x an y direction.
# Additionally, a range can be specified, if the ranges are not specified, it is
# assumed to be in [-1,1]   
def createGrid(nX, nY,rangeX=[-1,1],rangeY=[-1,1]):
    x = linspace(rangeX[0],rangeX[1],nX)
    y = linspace(rangeY[0],rangeY[1],nY)
    X,Y = meshgrid(x,y)
    return X,Y

# Create a circular aperture based on the grid X and Y. The radius is assumed at
# one, if it is not specified. Whether to include the boundary of the circle
# can be a topic of discussion. If desired, the returned datatype can be altered.
def circ(X,Y,radius = 1.,datatype = 'bool'):
    return array((X*X + Y*Y) <= (radius*radius),datatype)

# Preform a 2D inverse fourier transform based on existing fft classes in numpy.fft,
# Using this method is more cleaner and easier to implement in line: It preforms
# the shift in the fft (circular \pi-phase rotation) automatically.
def invsfft2(U,deltaF = 1):
    N = np.size(U,0)
    return np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(U))) * (N*deltaF)**2
    
def sfft2(u,deltaX = 1):
    N = np.size(U,0)
    return np.fft.fftshift(np.fft.fft2(np.fft.fftshift(u))) * (deltaX/N)**2