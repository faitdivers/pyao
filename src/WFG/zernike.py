from scipy import *
from numpy import *
import math

# Create Zernike Grid : Z_{u}^{v} = zernike(u,v,rho,theta)
# Compute the zernike mode based on the indices (u,v) at the specified location
# given by rho and theta. Accepts an ARRAY of locations rho and theta as wel as 
# scalar values.
# ISSUES:
# Some index mapping may be handy, i.e.: i -> (u,v)
def zernike(u,v,rho,theta):
    # The scaler of the part of the Zernike function, or not s dependant
    scalar = sqrt((2 * (u + 1)) / (1 + kroneckerDelta(v) ))
    # Determine of the (u,v)-combination is even or odd
    cond = ((u > 0) & (v > 0)) | ((v == 0) & (mod(u+2,4) == 0))

    # Now apply the even or odd scaler
    # TO DO: Merge condition into the if - statement 
    if cond:
        pol = cos(v*theta)
    else:
        pol = sin(v*theta)
    
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
def gamma(n):
    f = 1
    if n >=0:
        while n > 1:
            f = f * n
            n -= 1
        return f
    else:
        return inf
  
# Map Cartesian coordinates of polar coordinates : (r,t) = mapping(x,y)
# Computes the radius R and angle THETA from the (arrays) X and Y, representing
# the Cartesian coordinates. The index in the arrays couples the information in X and Y.      
def cart2pol(X,Y):
    R = sqrt(X*X + Y*Y)
    THETA = arctan2(Y,X)
    return R, THETA

# Map Cartesian coordinates of polar coordinates : (x,t) = mapping(r,t)
# Computes the X location and Y location from the (arrays) R and THETA, representing
# the polar coordinates. The index in the arrays couples the information in R and THETA.      
def pol2cart(R,THETA):
    X = R*cos(THETA)
    Y = R*sin(THETA)
    return X, Y
    