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
    }
    paramsSensor = lensletCentres(paramsSensor)
	
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

def lensletCentres(paramsSensor):
    # Unwrap paramsSensor
    numPupilx = paramsSensor['numPupilx'] # Samples on the x-axis
    numPupily = paramsSensor['numPupily'] # Samples on the y_axis
    lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
    ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
    f = paramsSensor['f'] # Focal length [m]
    D = paramsSensor['D'] # Lens diameter [m]
    lam = paramsSensor['lam'] # Wavelength [m]
    supportFactor = paramsSensor['supportFactor'] # Support factor
    D = paramsSensor['D'] # Lens diameter [m]
    dl = paramsSensor['dl'] # Distance between lenslets [m]
    noApertx = paramsSensor['noApertx'] # number of apertures in the x-direction
    noAperty = paramsSensor['noAperty'] # number of apertures in the y-direction
    numImagx = paramsSensor['numImagx'] # Samples on the x-axis
    numImagy = paramsSensor['numImagy'] # Samples on the y_axis	
    
    # Calculated missing parameters in paramsSensor	
    lensCentx = arange(noApertx)*(dl + D) + D/2 # Centers on x-axis [m]
    lensCenty = arange(noAperty)*(dl + D) + D/2 # Centers on y-axis [m]
    lensCentX, lensCentY = meshgrid(lensCentx, lensCenty) # Create rectangular grids for centres [m]
    lensCentx = hstack(lensCentX) # Stack the rectangular grids [m]
    lensCenty = hstack(lensCentY) # Stack the rectangular grids [m]
    lCalx = (noApertx - 1.0)*(dl + D) + D # Calculated length of array in x-direction [m]
    lCaly = (noAperty - 1.0)*(dl + D) + D # Calculated length of array in y-direction [m]
	
    # Set supplied array size to calculated array size if supplied array size
    # is smaller then the calculated array size
    if lx < lCalx: 
        lx = lCalx
    if ly < lCaly:
        ly = lCaly
	
    # Set new paramsSensor	
    paramsSensor = {
    # number of samples in the pupil plane
    'numPupilx' : numPupilx,
    'numPupily' : numPupily,
    # number of samples in the imaging plane(s)
    'numImagx' : numImagx,
    'numImagy' : numImagy,
    # number of apertures in the wfs
    'noApertx': noApertx,
    'noAperty': noAperty,
    # Focal Length [m]
    'f' : f,
    # Diameter of aperture of single lenslet [m]	
    'D' : D, 
    # Wavelength [m]	
    'lam' : lam, 	
    # Width of the lenslet array [m]
    'lx' : lx,
    'ly' : ly,
    # Distance between lenslets [m]	
    'dl' : dl,	
    # Normalized lenslet centers
    'lensCentx' : lensCentx/lx,
    'lensCenty' : lensCenty/ly,
    # Support factor used for support size [m] = support factor x diameter lenslet
    'supportFactor' : supportFactor,
    }
    return paramsSensor

def runClosedLoop(parameters, iterations):
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
