# -*- coding: utf-8 -*-
"""
Created on Thu May 22 09:15:51 2014

@author: admin
"""

from numpy import *
import numpy

from mainDM import *
from lensletConfig import *

def setup_params():
	""" Set-up the simulation parameters

	Setup the parameters used for all steps of the simulation.
	This includes parameters for the sensor, for the actuator and
	possibly other necessary simulation configuration.

	Returns:
		Multiple dicts, containing the parameters and their values.
	"""
        paramsWavefront = {
        # Scalar or array containing the zernike modes 
        'zernikeModes' : [2,4,21],
        # Scalar or array containing the zernike weights, with respect to the modes 
        'zernikeWeights' : [0.5,0.25,-0.6]
        }    
        
	paramsSensor = {
	# number of samples in the pupil plane
	'numPupilx' : 100, # Not used in WFS
	'numPupily' : 100, # Not used in WFS
	# number of samples in the imaging plane(s)
	'numImagx' : 100, # Not used in WFS
	'numImagy' : 100, # Not used in WFS
	# number of apertures in the wfs
	'noApertx': 5, # Not used in WFS
	'noAperty': 5, # Not used in WFS
	# Number of samples of the incoming phase
	'Nx' : 100,
	'Ny' : 100,
	# Focal Length [m]
	'f' : 18.0e-3,
	# Diameter of aperture of single lenslet [m]	
	'D' : 300.0e-6, 
	# Wavelength [m]	
	'lam' : 630.0e-9, 	
	# Distance between lenslets [m]	
	'dl' : 10.0e-6,	
 	# Width of the lenslet array [m]
	'lx' : 1.54e-3,
	'ly' : 1.54e-3,
	# Lenslet centers [m]

	}

	paramsActuator = {
	# number of actuators
	'numActx' : 5,
	'numActy' : 5,
	# parameters to characterize influence function
	}

	simulationParameters = {
	'frequency' : 10,       # Frequency of the simulation in Hertz
	'time' : 10             # Simulated time in seconds
	}

	# other sets of parameters may be defined if necessary

	# Encapsulate all the parameter dicts
	parameters = {
	'Wavefront' : paramsWavefront,
	'Sensor' : paramsSensor,
	'Actuator' : paramsActuator,
	'Simulation' : simulationParameters
	}

	return parameters
 
plt.close("all") # close all existing figures

parameters = setup_params()
wavefrontParameters = parameters['Wavefront'];
sensorParameters = parameters['Sensor'];
actuatorParameters = parameters['Actuator'];
simulationParameters = parameters['Simulation'];

lx, ly, lensCentx, lensCenty = lensletCentres(sensorParameters)
print("lensCentx:",lensCentx.shape)

# Normalized lenslet centers
sensorParameters['lensCentx'] = lensCentx
sensorParameters['lensCenty'] = lensCenty
# Set correct array widths
sensorParameters['lx'] = lx
sensorParameters['ly'] = ly

# call dm, note that lenslet positions is given 
wfDM = dm(0, sensorParameters, actuatorParameters)


