#Current Status for Single Lens System May 19, 2014
import math
from numpy import *
from scipy import *
import numpy.fft
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
from mainWFS import * 
import sys; sys.path.insert(0, '../')
from main import setup_params
	
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
	yo = arange(0.0,ly + dxo,dyo) # Sample positions on y-axis [m]
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
	phaseIn = zeros((size(Xo,0),size(Xo,1)))

	return Xo,Yo,phaseIn

# Run test
# Get parameters.
parameters = setup_params()
paramsSensor = parameters['Sensor'];
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
Xi,Yi,Ii = wfs(phaseIn, paramsSensor)
# Plot the intensity distribution
Ximm = Xi*1000.0
Yimm = Yi*1000.0
figIi = pl.figure()
conNum = pl.pcolor(Ximm,Yimm,Ii)
pl.title('Numerical Solution (mm)')
pl.show()
