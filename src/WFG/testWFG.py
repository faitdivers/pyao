from mainWFG import *
#from main import *
from numpy import *
from scipy import *
from zernike import *
from nollMap import *

import pylab as p
#import matplotlib.axes3d as p3
import mpl_toolkits.mplot3d.axes3d as p3

# Constants
#params,paramsAct = setup_params()
paramt = {
	'numPupilx' : 11,
	'numPupily' : 11,
	'numImagx' : 50,
	'numImagy' : 50,
	'noApertx': 5,
	'noAperty': 5
	}

# Show the values in paramt in the console
count = 0
print "Check properties of the test file:"  
for obj in paramt :
    print "\tprop(%d) | %r = %d" %(count,obj,paramt[obj])
    count += 1

# Test zernike function
# Change the zernike indices u and v or i here:
i = 7
u,v = zernikeIndex(i)
x = linspace(-1,1,paramt['numImagx'])
y = linspace(-1,1,paramt['numImagy'])
X,Y = meshgrid(x,y)
R,T = cart2pol(X,Y)
Zg = zernike(R,T,i)
title = 'Zernike Polynomial: u = %d, v = %d' %(u,v)

# Plot results in a surface plot
fig = p.figure();
ax = p3.Axes3D(fig)
ax.plot_surface(X,Y,Zg, rstride=1, cstride=1, cmap='jet')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel(title)
p.show()

# Test Noll's mapping
ul = 0
str = ""
for n in range(1,81):
    u,v = zernikeIndex(n)
    if ul != u:
        print(str)
        ul = u
        str = ""
    str = str + "%d: (%d,%d) " %(n,u,v)

# Test the total wfg routine here
#   DO NOT USE RESULTS! It will always be ones
res = wfg(paramt)
print "\nWave Front Generation:"
print "%r" %res

