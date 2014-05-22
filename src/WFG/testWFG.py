from mainWFG import *
#from main import *
from numpy import *
from scipy import *
from zernike import *
from nollMap import *

#import pylab as p
#import matplotlib.axes3d as p3
#import mpl_toolkits.mplot3d.axes3d as p3

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

#
# Show the values in paramt in the console
#
count = 0
print "Check properties of the test file:"  
for obj in paramt :
    print "\tprop(%d) | %r = %d" %(count,obj,paramt[obj])
    count += 1

#
# Create Zernike wavefront
#
i =4
zw = ZernikeWave()
zw.addMode([2,4,21],[0.5,0.25,-0.6])
zw.plotMode(i,paramt['numImagx'],paramt['numImagy'])

#
#zw.plotWavefront(paramt['numImagx'],paramt['numImagy'])
#
zw.plotWavefront(paramt['numImagx'],paramt['numImagy'])
WF = zw.createWavefront(paramt['numImagx'],paramt['numImagy'])
Z,A = zw.decomposeWavefront(WF)
print("\nThe wave front contains the following weights:")
print(reshape(A,(1,len(A))))
print("Check these with the weights you provided above:")
print(zw.getWeights())
print("Do they match?")
print(reshape(A,(1,len(A))) == zw.getWeights())
print("No? This is likely due to numerical inaccuracies!")

#
# Test Noll's mapping
#
ul = 0
str = ""
for n in range(1,81):
    u,v = zernikeIndex(n)
    if ul != u:
        print(str)
        ul = u
        str = ""
    str = str + "%d: (%d,%d) " %(n,u,v)

#
# Test the total wfg routine here
#   DO NOT USE RESULTS! It will always be ones
#
res = wfg(paramt)
print "\nWave Front Generation:"
print "%r" %res

