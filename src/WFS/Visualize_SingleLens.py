#Visualization for Single Lens System 
#Updated: June 20, 2014
#Project: PyAO
#Description: Allows for testing/visualization of a SingleLens intensity 
#			  distribution. Calls wfs from mainWFS.py for the numerical 
#			  intensities, then calculates the analytical intensities.
# 			  Plots both solutions and the error between them. This file 
#			  stands alone from the PyAO project main. 

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
		
		# Noise Parameters
		# Include Measurement Noise
		'Noisy': False, # True = include Readout, Photon noise, False = don't estimate measurement noise
		# Readout Noise Parameters (Modelled as Gaussian): based on CCD characteristics
		'sigma_readout': 0.005, # ratio of # readout noise electrons (nominally 0:5) to 
								# mean signal brightness (nominally 1000 electrons)
		'mean_readout': 0.0,   # should be 0 for white noise
		# Photon Noise Parameters (Modelled as Poisson): based only on expected value of Ii 
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
# Define Planar Wavefront
wf = zeros((paramsSensor['numPupilx'],paramsSensor['numPupily']))
# Get Numerical Solution - use WFSmain.py
xi, yi, Ii = wfs(wf, paramsSensor)
# Get Analytical Solution
Ia = analyticalLens(xi, yi, wf, paramsSensor)
# Calculate error between numerical and analytical solutions
I_err = Ii - Ia


# Prepare Plots
# Numerical Intensity Distribution
figIi = pl.figure()
conNum = pl.pcolor(xi*1000,yi*1000,Ii)
pl.xlabel('x (mm)')
pl.ylabel('y (mm)')
pl.title('Normalized Numerical Intensity Distribution')
pl.colorbar()

# Analytical Intensity Distribution
figIa = pl.figure()
conAna = pl.pcolor(xi*1000,yi*1000,Ia)
pl.xlabel('x (mm)')
pl.ylabel('y (mm)')
pl.title('Normalized Analytical Intensity Distribution')
pl.colorbar()

# Error between Intensity Distributions
figIa = pl.figure()
conAna = pl.pcolor(xi*1000,yi*1000,I_err)
pl.xlabel('x (mm)')
pl.ylabel('y (mm)')
pl.title('Error Between Normalized Numerical and Analytical Intensities')
pl.colorbar()

# Show all three plots
pl.show()
