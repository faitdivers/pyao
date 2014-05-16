from mainWFG import *
#from main import *
from zernike import *
from numpy import *
from scipy import *
import math

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
#   Change the zernike indices u and v here:
u = 2
v = 0
x = linspace(-1,1,paramt['numImagx'])
y = linspace(-1,1,paramt['numImagy'])
X,Y = meshgrid(x,y)
R,T = cart2pol(X,Y)

Zg = zernike(u,v,R,T)
title = 'Zernike Polynomial: u = %d, v = %d' %(u,v)

#   Plot results in a surface plot
fig = p.figure();
ax = p3.Axes3D(fig)
ax.plot_surface(X,Y,Zg, rstride=1, cstride=1, cmap='jet')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel(title)
p.show()

# Test the total wfg routine here
#   DO NOT USE RESULTS! It will always be ones
res = wfg(paramt)
print "\nWave Front Generation:"
print "%r" %res

