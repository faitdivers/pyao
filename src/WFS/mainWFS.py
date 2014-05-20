#Current Status for Single Lens System May 19, 2014
import math
from numpy import *
from scipy import *
import scipy.special #for the bessel function
import numpy.fft

import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

def wfs(phase, pS):
	# start parameter mapping (for now)
	D = pS['numPupilx']           # Diameter pupil[m], nominal value 300e-6
	f = pS['F']            # Focal length [m], nominal value 18e-3
	lam = pS['lam']        # Wavelength [m], nominal value 630e-9
	N_x = pS['numPupilx']  # Number of samples
	N_y = pS['numPupily']  # Number of samples
	L_x = pS['Lx']
	L_y = pS['Ly']
	k = 2*pi/lam        # Wavenumber

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


	# TBD: Should each lenslet get only the WF in front of its aperture? 
	#     or get the WHOLE (or all neighbours) Wavefront?
	
	# ---------------------------------------------------------------------------------------------
	# Loop from here across each lenslet
	
	# keep this only until loop ready (& change variable names)
	#U_i = phase at current lenslet		  
	U_i = 1			# Unit input
	
	# Complex Amplitude just before the lens
	U_lb = P * U_i                          # Complex amplitude just before the lens
	
	# 2D Fast Fourier transform for the field behind the lens
	U_la = delta_x*delta_y*numpy.fft.fftshift(numpy.fft.fft2(U_lb))
	
	# NUMERICAL SOLUTION
	# Complete with multiplicative factor for Fraunhofer diffraction patterns at the focal plane
	# Which in this case equals the Fresnel diffraction patterns

	U_i = exp(1j*k*f)*exp(1j*k*(F_x**2 + F_y**2)*lam**2*f/2)/(1j*lam*f)*U_la
	I_i = absolute(U_i)**2 					# Intensity profile in the focal plane, numerically
	X_i = F_x*lam*f
	Y_i = F_y*lam*f
	
	# end of needed loop
	# ---------------------------------------------------------------------------------------------

	
	# Return variable: I_i
	
	# sytnax: ones(shape, dtype=None, order='C')
	# Phase may not be of same dimension as Intensities, I believe
	# 	Phase is related to wf which comes from the pupil plane sample #
	#	Intensities are related to the # samples in the imaging plane
	return ones(phase.shape)
