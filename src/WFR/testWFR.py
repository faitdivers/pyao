from mainWFR import *

def setup_params():
	""" Set-up the simulation parameters

	Returns:
		Multiple dicts, containing the parameters and their values.
	"""

	paramsSensor = {
	# number of samples in the pupil plane
	'numPupilx' : 100,
	'numPupily' : 100,
	# number of samples in the imaging plane(s)
	'numImagx' : 100,
	'numImagy' : 100,
	# number of apertures in the wfs
	'noApertx': 10,
	'noAperty': 10,
	# focal distance, pixel length, sizes/diameters of the apertures, ...
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
