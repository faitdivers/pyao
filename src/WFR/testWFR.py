from mainWFR import *

def setup_params():
	""" Set-up the simulation parameters

	Setup the parameters used for all steps of the simulation.
	This includes parameters for the sensor, for the actuator and
	possibly other necessary simulation configuration.

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
	'noApertx': 2,
	'noAperty': 2,
	# focal distance, pixel length, sizes/diameters of the apertures, ...
	}

	paramsActuator = {
	# number of actuators
	'numActx' : 8,
	'numActy' : 8,
	# parameters to characterize influence function
	}

	simulationParameters = {
	'frequency' : 10,       # Frequency of the simulation in Hertz
	'time' : 10             # Simulated time in seconds
	}

	# other sets of parameters may be defined if necessary

	# Encapsulate all the parameter dicts
	parameters = {
	'Sensor' : paramsSensor,
	'Actuator' : paramsActuator,
	'Simulation' : simulationParameters
	}

	return parameters

def test_run():
	# Get parameters.
	parameters = setup_params()
	sensorParameters = parameters['Sensor'];
	actuatorParameters = parameters['Actuator'];
	simulationParameters = parameters['Simulation'];

	centroids = ones((sensorParameters['noApertx']*sensorParameters['noAperty']*2,1))
	wfRec = wfr(centroids, sensorParameters)
	return

test_run()
