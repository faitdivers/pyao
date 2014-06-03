# Main file for PyAO toolbox

from numpy import *
import matplotlib.pyplot as pl

from WFG.mainWFG import *
from WFS.mainWFS import *
from Centroid.mainCentroid import *
from WFR.mainWFR import *
from Control.mainControl import *
from DM.mainDM import *


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
    'numPupilx': 100,
    'numPupily': 100,
    # number of samples in the imaging plane(s)
    'numImagx': 100,
    'numImagy': 100,
    # number of apertures in the wfs
    'noApertx': 10,
    'noAperty': 10,
    # focal distance, pixel length, sizes/diameters of the apertures, ...
    'F': 18e-3,            # Focal Length [m]
    'Diam': 300e-6,     # Diameter of pupil [m] - of system or lenslet?
    'lam': 630e-9,         # Wavelength [m]
    'Lx': 4000e-6,         # Support Width in x dimension (real space) [m]
    'Ly': 4000e-6,         # Support Width in y dimension (real space) [m]
    }

    paramsActuator = {
    # number of actuators
    'numActx': 8,
    'numActy': 8,
    # parameters to characterize influence function
    }

    simulationParameters = {
    'frequency': 10,       # Frequency of the simulation in Hertz
    'time': 10,             # Simulated time in seconds
    'is_closed_loop': False
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


def runClosedLoop(parameters, iterations):
    """ Run a closed-loop simulation

    The closed-loop simulation consists of
    1. generating the wafe-front
    2. applying the deformable mirror to the wafe-front
    3. a) measuring intensities
    3. b) determining centroids
    4. reconstructing the wafe-front
    5. calculate the control values for the actuators,
    6. actuate the mirror
    7. continue from step 1

    The stop condition is the simulation time.
    """
    # Get parameters.
    wavefrontParameters = parameters['Wavefront']
    sensorParameters = parameters['Sensor']
    actuatorParameters = parameters['Actuator']

    # The first deformable mirror effect: (No effect)
    wfDM = dm(0, sensorParameters)

    for i in range(0, iterations):
        print("Running simulation step %d" % (i))
        wf = wfg(sensorParameters, wavefrontParameters['zernikeModes'],
                 wavefrontParameters['zernikeWeights'])
        wfRes = wf - wfDM
        intensities = wfs(wfRes, sensorParameters)
        centroids = centroid(intensities, sensorParameters)
        wfRec = wfr(centroids, sensorParameters)
        actCommands = control(wfRec, actuatorParameters)
        wfDM = dm(actCommands, sensorParameters)
    return


def runOpenLoop(parameters, iterations):
    """ Run an open-loop simulation

    The open-loop simulation consists of
    1. generating the wafe-front
    2. applying the deformable mirror to the wafe-front
    3. a) measuring intensities
    3. b) determining centroids
    4. reconstructing the wafe-front
    5. actuate the mirror
    6. continue from step 1

    The stop condition is the simulation time.
    """
    wavefrontParameters = parameters['Wavefront']
    sensorParameters = parameters['Sensor']
    actuatorParameters = parameters['Actuator']

    print("Running open loop simulation")
    # The first deformable mirror effect: (No effect)
    wfDM = dm(0, sensorParameters)

    for i in range(0, iterations):
        print("Running simulation step %d" % (i))
        wf = wfg(sensorParameters, wavefrontParameters['zernikeModes'],
                 wavefrontParameters['zernikeWeights'])
        wfRes = wf - wfDM
        intensities = wfs(wfRes, sensorParameters)
        centroids = centroid(intensities, sensorParameters)
        wfRec = wfr(centroids, sensorParameters)
        wfDM = dm(0, sensorParameters)
    return


def run_simulation(parameters):
    """ Runs the configured simulation. Either an open or closed loop.

    """
    simulation_parameters = parameters['Simulation']
    iterations = (simulation_parameters['frequency'] *
                  simulation_parameters['time'])

    if simulation_parameters['is_closed_loop']:
        runClosedLoop(parameters, iterations)
    else:
        runOpenLoop(parameters, iterations)


parameters = setup_params()
run_simulation(parameters)
