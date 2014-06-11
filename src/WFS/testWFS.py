#Current Status for Single Lens System May 19, 2014
import math
from numpy import *
from scipy import *
import numpy.fft
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
from mainWFS import * 

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
	
def lensletCentres(paramsSensor):
	# Unwrap paramsSensor
	numPupilx = paramsSensor['numPupilx'] # Samples on the x-axis
	numPupily = paramsSensor['numPupily'] # Samples on the y_axis
	lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
	ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
	f = paramsSensor['f'] # Focal length [m]
	D = paramsSensor['D'] # Lens diameter [m]
	lam = paramsSensor['lam'] # Wavelength [m]
	supportFactor = paramsSensor['supportFactor'] # Support factor
	D = paramsSensor['D'] # Lens diameter [m]
	dl = paramsSensor['dl'] # Distance between lenslets [m]
	noApertx = paramsSensor['noApertx'] # number of apertures in the x-direction
	noAperty = paramsSensor['noAperty'] # number of apertures in the y-direction
	numImagx = paramsSensor['numImagx'] # Samples on the x-axis
	numImagy = paramsSensor['numImagy'] # Samples on the y_axis	
	
	# Calculated missing parameters in paramsSensor	
	lensCentx = arange(noApertx)*(dl + D) + D/2 # Centers on x-axis [m]
	lensCenty = arange(noAperty)*(dl + D) + D/2 # Centers on y-axis [m]
	lensCentX, lensCentY = meshgrid(lensCentx, lensCenty) # Create rectangular grids for centres [m]
	lensCentx = hstack(lensCentX) # Stack the rectangular grids [m]
	lensCenty = hstack(lensCentY) # Stack the rectangular grids [m]
	lCalx = (noApertx - 1.0)*(dl + D) + D # Calculated length of array in x-direction [m]
	lCaly = (noAperty - 1.0)*(dl + D) + D # Calculated length of array in y-direction [m]
	
	# Set supplied array size to calculated array size if supplied array size
	# is smaller then the calculated array size
	if lx < lCalx: 
		lx = lCalx
	if ly < lCaly:
		ly = lCaly
	
	# Set new paramsSensor	
	paramsSensor = {
		# number of samples in the pupil plane
		'numPupilx' : numPupilx,
		'numPupily' : numPupily,
		# number of samples in the imaging plane(s)
		'numImagx' : numImagx,
		'numImagy' : numImagy,
		# number of apertures in the wfs
		'noApertx': noApertx,
		'noAperty': noAperty,
		# Focal Length [m]
		'f' : f,
		# Diameter of aperture of single lenslet [m]	
		'D' : D, 
		# Wavelength [m]	
		'lam' : lam, 	
		# Width of the lenslet array [m]
		'lx' : lx,
		'ly' : ly,
		# Distance between lenslets [m]	
		'dl' : dl,	
		# Normalized lenslet centers
		'lensCentx' : lensCentx/lx,
		'lensCenty' : lensCenty/ly,
		# Support factor used for support size [m] = support factor x diameter lenslet
		'supportFactor' : supportFactor,
	}
	return paramsSensor
	
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
paramsSensor = lensletCentres(paramsSensor)
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
