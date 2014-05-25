#from scipy import *
#from numpy import *
from math import *

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