#Visualization for Single Lens System 
#Updated: June 18, 2014
#Project: PyAO
#Description: Allows for testing/visualization of a SingleLens solution. 
#             Calls wfs from mainWFS.py for the numerical solution, 
#			  then calculates the analytical solution and plots both 
#             solutions. This file stands alone from the PyAO project main. 

from mainWFS import *
from lensArrayConfig import *

import math
from numpy import *
#from scipy import *
import scipy.special   # for the bessel function
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

# This function generates the sensor parameters. Directly copied from main.py
def setup_params():
	paramsSensor = {
		# number of samples in the pupil plane
		'numPupilx' : 200,
		'numPupily' : 200,
		# number of samples in the imaging plane(s)
		'numImagx' : 200,
		'numImagy' : 200,
		# number of apertures in the wfs
		'noApertx': 1,
		'noAperty': 1,
		# Focal Length [m]
		'f' : 18.0e-3,
		# Diameter of aperture of single lenslet [m]	
		'D' : 300.0e-6, 
		# Wavelength [m]	
		'lam' : 630.0e-9, 	
		# Width of the lenslet array [m]
		'lx' : 0.3e-3,
		'ly' : 0.3e-3,
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
	
	return paramsSensor

	
	
# This function generates a test phase (wavefront) for the test run. 
# Directly copied from testWFS.py
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

	
	
# This function calculates the analytical solution for the intensity distribution 
# of a single lens through a circular aperture.  Takes the sampling positions 
# (xi, yi) generated from the numerical solution for consistency. 
# Based on the Matlab Code developed by Nick Kant.
def analyticalLens (xi, yi, wf, paramsSensor):
# unwrap parameters
	D = paramsSensor['D']    	 # Diameter pupil[m], nominal value 300e-6
	f = paramsSensor['f']        # Focal length [m], nominal value 18e-3
	lam = paramsSensor['lam']    # Wavelength [m], nominal value 630e-9
	k = 2*pi/lam          		 # Wavenumber

	# Determine offsets for centering grid at (0,0) for analytical PSF
	o_x = max(xi/2)
	o_y = max(yi/2)
	
	# Create Spatial Grid (offset of half the 
	X_i, Y_i = meshgrid(xi - o_x, yi - o_y)   

	# Calculate Analytical Intensity Distribution
	# Fraunhofer diffraction pattern of a circular aperture
	A = pi*((D/2)**2)
	r = sqrt(X_i**2 + Y_i**2)
	Ia = (A/(lam*f))**2*(2*scipy.special.j1(k*(D/2)*r/f)/(k*(D/2)*r/f))**2 

	Ia = Ia/amax(absolute(Ia)) # Normalize intensity distribution

	return Ia
	
# Define Parameters
paramsSensor = setup_params()
# Generate Wavefront
xo, yo, wf = createTestPhase(paramsSensor)
# Get Numerical Solution - use WFSmain.py
xi, yi, Ii = wfs(wf, paramsSensor)
# Get Analytical Solution
Ia = analyticalLens(xi, yi, wf, paramsSensor)

# Plotting
# Plot Wavefront
figPhaseIn = pl.figure()
ax = figPhaseIn.gca(projection='3d')
surf = ax.plot_surface(xo*1000,yo*1000,wf)
ax.set_xlabel('x [mm]')
ax.set_ylabel('y [mm]')
ax.set_zlabel('Phase')
ax.set_title('Incident Wavefront Phase')

# Plot Numerical Intensity Distribution
figIi = pl.figure()
conNum = pl.pcolor(xi*1000,yi*1000,Ii)
pl.xlabel('x (mm)')
pl.ylabel('y (mm)')
pl.title('Normalized Numerical Intensity Distribution')
pl.colorbar()

# Plot Analytical Solution
figIa = pl.figure()
conAna = pl.pcolor(xi*1000,yi*1000,Ia)
pl.xlabel('x (mm)')
pl.ylabel('y (mm)')
pl.title('Normalized Analytical Intensity Distribution')
pl.colorbar()

pl.show()
