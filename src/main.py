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
    'time': 10             # Simulated time in seconds
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


def runClosedLoop():
    """ Run a closed loop simulation

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
    parameters = setup_params()
    wavefrontParameters = parameters['Wavefront']
    sensorParameters = parameters['Sensor']
    actuatorParameters = parameters['Actuator']
    simulationParameters = parameters['Simulation']

    # Calculate number of simulation steps
    iterations = (simulationParameters['time'] *
                  simulationParameters['frequency'])

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


def runOpenLoop():
    parameters = setup_params()
    wavefrontParameters = parameters['Wavefront']
    sensorParameters = parameters['Sensor']
    actuatorParameters = parameters['Actuator']

    print("Running open loop simulation")
    # Generate wavefront
    wf = wfg(sensorParameters, wavefrontParameters['zernikeModes'],
             wavefrontParameters['zernikeWeights'])
    #pl.imshow(wf), pl.show(), pl.title('Incoming wavefront')
    # Generate intensity measurements
    intensities = wfs(wf, sensorParameters)
    # Compute centroids (this step is not needed if we are to use focal
    # plane reconstruction techniques)
    centroids = centroid(intensities, sensorParameters)
    #print centroids.shape
    # Reconstruct the wavefront
    wfRec = wfr(centroids, sensorParameters)
    # Compute the actuator commands via a control technique
    actCommands = control(wfRec, actuatorParameters)
    # Deformable mirror
    wfDM = dm(actCommands, sensorParameters)
    # Compute the residual wavefront
    wfRes = wf - wfDM
    return

runClosedLoop()
