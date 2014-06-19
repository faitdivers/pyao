#Current Status for Single Lens System May 19, 2014
import math
from numpy import *
from scipy import *
import numpy.fft
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
from mainWFS import * 
from lensArrayConfig import *

paramsSensor = {
	# number of samples in the pupil plane
	'numPupilx' : 200,
	'numPupily' : 200,
	# number of samples in the imaging plane(s)
	'numImagx' : 200,
	'numImagy' : 200,
	# number of apertures in the wfs
	'noApertx': 5,
	'noAperty': 5,
	# Focal Length [m]
	'f' : 18.0e-3,
	# Diameter of aperture of single lenslet [m]	
	'D' : 300.0e-6, 
	# Wavelength [m]	
	'lam' : 630.0e-9, 	
	# Width of the lenslet array [m]
	'lx' : 0.54e-3,
	'ly' : 0.24e-3,
	# Distance between lenslets [m]	
	'dl' : 10.0e-6,	
	# Support factor used for support size [m] = support factor x diameter lenslet
	'supportFactor' : 4,
	}
# Compute lenslet centres and check minimal array widths 
lx, ly, lensCentx, lensCenty = lensletCentres(paramsSensor)
# Normalized lenslet centers
paramsSensor['lensCentx'] = lensCentx
paramsSensor['lensCenty'] = lensCenty
# Set correct array widths
paramsSensor['lx'] = lx
paramsSensor['ly'] = ly
	
def createTestPhase(paramsSensor):
	# Unwrap paramsSensor
	Nx = paramsSensor['numPupilx'] # Samples on the x-axis per lenslet
	Ny = paramsSensor['numPupily'] # Samples on the y_axis per lenslet
	lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
	ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
	lam = paramsSensor['lam'] # Wavelength [m]
	k = 2*pi/lam # Wavenumber
	
	dxo = lx/(Nx - 1.0) # Sample length on x-axis [m]
	dyo = ly/(Ny - 1.0) # Sample length on y-axis [m]
	xo = arange(0.0,lx + dxo,dxo) # Sample positions on x-axis [m]
	yo = arange(0.0,ly + dyo,dyo) # Sample positions on y-axis [m]
	Xo, Yo = meshgrid(xo,yo) # Create spatial grid
	
	# Create random wavefront
#	ax = random.uniform(-1.0,1.0)*2.0
#	ay = random.uniform(-1.0,1.0)*2.0
#	bx = random.uniform(-1.0,1.0)*1.0
#	by = random.uniform(-1.0,1.0)*1.0
#	cx = random.uniform(-1.0,1.0)*0.0001 # Tilt x
#	cy = random.uniform(-1.0,1.0)*0.0001 # Tilt y
#	ex = random.uniform(-1.0,1.0)*2.0
#	ey = random.uniform(-1.0,1.0)*2.0
#	d =  random.uniform(-1.0,1.0)
#
#	phaseIn = k*((ax*Xo)**3.0 + (ay*Yo)**3.0 + (bx*Xo)**2.0 + 
#		(by*Yo)**2.0 + cx*Xo + cy*Yo + d + (ex*Xo)**4.0 + (ey*Yo)**4.0)
	
	# Create a planar wavefront
	phaseIn = zeros((size(yo),size(xo)))

	return Xo,Yo,phaseIn

# Run test
# Create a icident phase
Xo,Yo,phaseIn = createTestPhase(paramsSensor)
# Plot the incident pahse
figPhaseIn = pl.figure()
ax = figPhaseIn.gca(projection='3d')
surf = ax.plot_surface(Xo,Yo,phaseIn, rstride=1, cstride=1, cmap='jet')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Phase')
pl.show()
# Create the intensity distribution
X,Y,Ii = wfs(phaseIn, paramsSensor)
# Plot the intensity distribution
Xmm = X*1000.0
Ymm = Y*1000.0
figIi = pl.figure()
conNum = pl.pcolor(Xmm,Ymm,Ii)
pl.title('Numerical Solution (mm)')
pl.show()
