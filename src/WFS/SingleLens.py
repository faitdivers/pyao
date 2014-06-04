#Single Lens System 
#Updated: May 28, 2014
#Project: PyAO
#Description: Given the numerical solution for the intensities, the incoming 
#             wavefront and the sensor parameters, computes the analytical 
#             solution for the intensity distribution and plots the numerical 
#             and analytical solutions

import math
from numpy import *
from scipy import *
import scipy.special #for the bessel function
import numpy.fft

import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D



def wfs_Plot(I_i, U_i, pS):
	# unwrap parameters
	D = pS['Diam']    	   # Diameter pupil[m], nominal value 300e-6
	f = pS['F']            # Focal length [m], nominal value 18e-3
	lam = pS['lam']        # Wavelength [m], nominal value 630e-9
	N_x = pS['numPupilx']  # Number of samples
	N_y = pS['numPupily']  # Number of samples
	L_x = pS['Lx']
	L_y = pS['Ly']
	k = 2*pi/lam           # Wavenumber

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

	X_i = F_x*lam*f
	Y_i = F_y*lam*f

	# ---------------------------------------------------------------------------------------------
	# Prepare Plot of Numerical Solution
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
