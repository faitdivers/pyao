from mainWFR import *

def setup_params():
	""" Set-up the simulation parameters

	Returns:
		Multiple dicts, containing the parameters and their values.
	"""

	paramsSensor = {
	# number of samples in the pupil plane
	'numPupilx' : 100, # Not used in WFS
	'numPupily' : 100, # Not used in WFS
	# number of samples in the imaging plane(s)
	'numImagx' : 100, # Not used in WFS
	'numImagy' : 100, # Not used in WFS
	# number of apertures in the wfs
	'noApertx': 10, # Not used in WFS
	'noAperty': 10, # Not used in WFS
	# Number of samples of the incoming phase
	'Nx' : 100,
	'Ny' : 100,
	# Focal Length [m]
	'f' : 18.0e-3,
	# Diameter of aperture of single lenslet [m]	
	'D' : 300.0e-6, 
	# Wavelength [m]	
	'lam' : 630.0e-9, 	
	# Width of the lenslet array [m]
	'lx' : 1.54e-3,
	'ly' : 1.54e-3,
	# Lenslet centers [m]
	'lensCentx' : [ 0.00015,  0.00046,  0.00077,  0.00108,  0.00139],
	'lensCentx' : [ 0.00015,  0.00046,  0.00077,  0.00108,  0.00139],
	}

	# Encapsulate all the parameter dicts
	parameters = {
	'Sensor' : paramsSensor,
	}

	return parameters

def test_run():
	# Get parameters.
	parameters = setup_params()
	sensorParameters = parameters['Sensor'];

	centroids = ones((sensorParameters['noApertx']*sensorParameters['noAperty']*2,1))
	wfRec = wfr(centroids, sensorParameters)
	return

test_run()
