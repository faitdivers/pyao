from mainWFR import *
from plotWavefront import *
from determinePhiPositions import determine_phi_positions
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
from WFS.lensArrayConfig import *

def setup_params():
	""" Set-up the simulation parameters

	Returns:
		Multiple dicts, containing the parameters and their values.
	"""

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
	# Illumination threshold (fractional flux threshold)
	'illumThreshold' : 0.3,
	}
	
	# Compute lenslet centres and check minimal array widths 
	lx, ly, lensCentx, lensCenty = lensletCentres(paramsSensor)
	# Normalized lenslet centers
	paramsSensor['lensCentx'] = lensCentx
	paramsSensor['lensCenty'] = lensCenty
	# Set correct array widths
	paramsSensor['lx'] = lx
	paramsSensor['ly'] = ly
	
	# Encapsulate all the parameter dicts
	parameters = {
	'Sensor' : paramsSensor,
	}

	return parameters

def test_run():
	# Get parameters.
	parameters = setup_params()
	sensorParameters = parameters['Sensor'];
	
	geometry = 'fried'
	
	phiCentersX, phiCentersY = determine_phi_positions(sensorParameters['lensCentx'], sensorParameters['lx'], sensorParameters['noApertx'], sensorParameters['lensCenty'], sensorParameters['ly'], sensorParameters['noAperty'], sensorParameters['dl'], sensorParameters['D'], geometry)

	y_slopes = ones((sensorParameters['noApertx']*sensorParameters['noAperty'],1))
	x_slopes = zeros((sensorParameters['noApertx']*sensorParameters['noAperty'],1))
	centroids = vstack([x_slopes, y_slopes])
	wfRec = wfr(centroids, sensorParameters, geometry)
	plotWavefront(phiCentersX,phiCentersY,wfRec,sensorParameters['noApertx'],sensorParameters['noAperty'],geometry)
	return

test_run()
