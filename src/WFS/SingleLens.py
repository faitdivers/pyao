#Current Status for Single Lens System May 19, 2014
import math
from numpy import *
from scipy import *
import scipy.special #for the bessel function
import numpy.fft

import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D


def SingleLens(U_i, N):
	# start parameter mapping (for now)
	D = 300e-6        # Diameter pupil[m], nominal value 300e-6
	f = 18e-3         # Focal length [m], nominal value 18e-3
	lam = 630e-9      # Wavelength [m], nominal value 630e-9
	#N = 100            # Number of samples
	L = 4000e-6       # Support width in real space [m]
	N_x = N
	N_y = N
	L_x = L
	L_y = L
	k = 2*pi/lam      # Wavenumber

	# Prepare Spatial Grid
	delta_x = L_x/N_x                      # Sample spacing [m]
	delta_y = L_y/N_y                      # Sample spacing [m]
	x = arange(-L_x/2, L_x/2, delta_x)     # Spatial positions [m]
	y = arange(-L_y/2, L_y/2, delta_y)     # Spatial positions [m]
	X,Y = meshgrid(x,y)                    # Spatial grid [m]

	# Prepare Frequency Grid
	delta_f_x = 1/L_x                      						# Sample spacing [rad/m]        
	delta_f_y = 1/L_y                     						# Sample spacing [rad/m]
	f_x = arange(-1.0/2.0/delta_x, 1.0/2.0/delta_x, delta_f_x)  # Spatial frequencies [rad/m]
	f_y = arange(-1.0/2.0/delta_y, 1.0/2.0/delta_y, delta_f_y)  # Spatial frequencies [rad/m]
	F_x,F_y = meshgrid(f_x,f_y)          						# Frequency grid [rad/m]

	# Define Pupil Function
	# Create grid of the pupil function
	P = sqrt(X**2 + Y**2) <= D/2  # circle
	#P = logical_and(logical_and(X <= D, X >= -D), logical_and(Y <= D,  Y >= -D)) # square of width 2D

	#U_i = phase at current lenslet		  
	#U_i = 1			# Unit input

	# Complex Amplitude just before the lens
	U_lb = P * U_i                          # Complex amplitude just before the lens

	# 2D Fast Fourier transform for the field behind the lens
	U_la = delta_x*delta_y*numpy.fft.fftshift(numpy.fft.fft2(U_lb))

	# ---------------------------------------------------------------------------------------------
	# NUMERICAL SOLUTION
	# Complete with multiplicative factor for Fraunhofer diffraction patterns at the focal plane
	# Which in this case equals the Fresnel diffraction patterns

	U_i = exp(1j*k*f)*exp(1j*k*(F_x**2 + F_y**2)*lam**2*f/2)/(1j*lam*f)*U_la
	I_i = absolute(U_i)**2 					# Intensity profile in the focal plane, numerically
	X_i = F_x*lam*f
	Y_i = F_y*lam*f

	# Plot of Numerical Solution
	figNum = pl.figure()
	ax = figNum.gca(projection='3d')
	surf = ax.plot_surface(X_i,Y_i,I_i, rstride=1, cstride=1, cmap='jet')
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('Numerical Solution')
	ax.view_init(90, -90)

	# ---------------------------------------------------------------------------------------------
	# ANALYTICAL SOLUTION
	# Fraunhofer diffraction pattern of a circular aperture
	A = pi*((D/2)**2)
	r = sqrt(X_i**2 + Y_i**2)
	# Intensity profile in the focal plane, analytically
	I_A = (A/(lam*f))**2*(2*scipy.special.j1(k*(D/2)*r/f)/(k*(D/2)*r/f))**2 

	# Plot of Analytical Solution
	figAna = pl.figure()
	ax = figAna.gca(projection='3d')
	surf = ax.plot_surface(X_i,Y_i,I_A, rstride=1, cstride=1, cmap='jet')
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('Analytical Solution')
	ax.view_init(90, -90)
	# ---------------------------------------------------------------------------------------------

	# Print Plot & Prepare Return variable
	pl.show()


SingleLens(1,50)