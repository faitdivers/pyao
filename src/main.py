# Main file for PyAO toolbox

import numpy

from WFG.mainWFG import *
from WFS.mainWFS import *
from WFS.lensArrayConfig import *
from Centroid.mainCentroid import *
from WFR.mainWFR import *
from Control.mainControl import *
from DM.mainDM import *
from Simulation.LatencyBuffer import LatencyBuffer


def setup_params():
    """ Set-up the simulation parameters

    Setup the parameters used for all steps of the simulation.
    This includes parameters for the sensor, for the actuator and
    possibly other necessary simulation configuration.

    Returns:
        Multiple dictionaries, containing the parameters and their values.
    """
    paramsWavefront = {
    # Scalar or array containing the zernike modes
    'zernikeModes': [2, 4, 21],
    # Scalar or array containing the zernike weights, with respect to the modes
    'zernikeWeights': [0.5, 0.25, -0.6]
    }

    paramsSensor = {
    # number of samples in the pupil plane
    'numPupilx' : 200,
    'numPupily' : 200,
    # number of samples in the imaging plane(s)
    'numImagx' : 200,
    'numImagy' : 200,
    # number of apertures in the wfs
    'noApertx': 4,
    'noAperty': 4,
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
    

    paramsActuator = {
    # number of actuators
    'numActx': 8,
    'numActy': 8,
    # parameters to characterize influence function
    }

    simulationParameters = {
    'frequency': 10,       # Frequency of the simulation in Hertz
    'time': 10,            # Simulated time in seconds
    'delay': 0,  # Delay in number of samples
    'is_closed_loop': True
    }

    # other sets of parameters may be defined if necessary

    # Encapsulate all the parameter dicts
    parameters = {
    'Wavefront': paramsWavefront,
    'Sensor': paramsSensor,
    'Actuator': paramsActuator,
    'Simulation': simulationParameters
    }

    return parameters


def runClosedLoop(parameters, iterations, buffer_size):
    """ Run a closed-loop simulation

    The closed-loop simulation consists of
    1. generating the wave-front
    2. applying the deformable mirror to the wave-front
    3. a) measuring intensities
    3. b) determining centroids
    4. reconstructing the wave-front
    5. calculate the control values for the actuators,
    6. actuate the mirror
    7. repeat from step 1

    The stop condition is the simulation time.
    """
    # Get parameters.
    wavefrontParameters = parameters['Wavefront']
    sensorParameters = parameters['Sensor']
    actuatorParameters = parameters['Actuator']

    wf_buffer = []
    intensities_buffer = []
    centroids_buffer = []
    reconstructed_buffer = []
    wf_dm_buffer = []
    
    print("Running closed-loop simulation")
    # The first deformable mirror effect: (No effect)
    wfDM = dm(0, sensorParameters)

    delay_buffer = LatencyBuffer(buffer_size, (sensorParameters['numPupilx'],
                                     sensorParameters['numPupilx']))
    for i in range(0, iterations):
        print("Running simulation step %d" % (i))
        wf = wfg(sensorParameters, wavefrontParameters['zernikeModes'],
                 wavefrontParameters['zernikeWeights'])
        wfRes = wf - wfDM
        xInt, yInt, intensities = wfs(wfRes, sensorParameters)
        centroids = centroid(intensities, sensorParameters)
        wfRec = wfr(centroids, sensorParameters)
        wfRec = delay_buffer.update(wfRec)
        actCommands = control(wfRec, actuatorParameters)
        wfDM = dm(actCommands, sensorParameters)

        wf_buffer.append(wf)
        intensities_buffer.append(intensities)
        centroids_buffer.append(centroids)
        reconstructed_buffer.append(wfRec)
        wf_dm_buffer.append(wfDM)

    results = pack_simulation_results(wf_buffer, intensities_buffer,
                                    centroids_buffer, reconstructed_buffer,
                                    wf_dm_buffer)
    return results


def runOpenLoop(parameters, iterations, buffer_size):
    """ Run an open-loop simulation

    The open-loop simulation consists of
    1. generating the wave-front
    2. applying the deformable mirror to the wave-front
    3. a) measuring intensities
    3. b) determining centroids
    4. reconstructing the wave-front
    5. actuate the mirror
    6. repeat from step 1

    The stop condition is the simulation time.
    """
    wavefrontParameters = parameters['Wavefront']
    sensorParameters = parameters['Sensor']
    actuatorParameters = parameters['Actuator']

    delay_buffer = LatencyBuffer(buffer_size, (sensorParameters['numPupilx'],
                                     sensorParameters['numPupilx']))

    wf_buffer = []
    intensities_buffer = []
    centroids_buffer = []
    reconstructed_buffer = []
    wf_dm_buffer = []

    print("Running open-loop simulation")
    # The first deformable mirror effect: (No effect)
    wfDM = dm(0, sensorParameters)

    for i in range(0, iterations):
        print("Running simulation step %d" % (i))
        wf = wfg(sensorParameters, wavefrontParameters['zernikeModes'],
                 wavefrontParameters['zernikeWeights'])
        wfRes = wf - wfDM
        xInt, yInt, intensities = wfs(wfRes, sensorParameters)
        centroids = centroid(intensities, sensorParameters)
        wfRec, phiCentersX, phiCentersY = wfr(centroids, sensorParameters)
        wfRec = delay_buffer.update(wfRec)
        wfDM = dm(0, sensorParameters)

        wf_buffer.append(wf)
        intensities_buffer.append(intensities)
        centroids_buffer.append(centroids)
        reconstructed_buffer.append(wfRec)
        wf_dm_buffer.append(wfDM)

    results = pack_simulation_results(wf_buffer, intensities_buffer,
                                    centroids_buffer, reconstructed_buffer,
                                    wf_dm_buffer)
    return results


def pack_simulation_results(wf, intensities, centroids, reconstructed, wf_dm):
    simulation_results = {
    'wf': wf,
    'intensities': intensities,
    'centroids': centroids,
    'reconstructed': reconstructed,
    'wf_dm': wf_dm
    }

    return simulation_results


def run_simulation(parameters):
    """ Runs the configured simulation. Either an open or closed loop.

    """
    simulation_parameters = parameters['Simulation']
    iterations = int(simulation_parameters['frequency'] *
                  simulation_parameters['time'])

    delay_buffer_size = simulation_parameters['delay'] + 1

    if simulation_parameters['is_closed_loop']:
        runClosedLoop(parameters, iterations, delay_buffer_size)
    else:
        runOpenLoop(parameters, iterations, delay_buffer_size)


parameters = setup_params()
run_simulation(parameters)
