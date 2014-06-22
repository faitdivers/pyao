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
from WFR.determinePhiPositions import determine_phi_positions
import matplotlib.pyplot as pl
import time
from Control.PIDController import PIDcontroller

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
    'zernikeWeights': [0.0005, 0.00025, -0.0006]
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
    'sig1_multiplier': 0.54,
    'sig2_multiplier': 0.85,
    'w1': 2,
    'w2': -1
    }

    reconstructionParameters = {
    #The geometry that is used for reconstruction (choose: fried, southwell, mhudgin)
    'geometry': 'southwell'
    }
    
    simulationParameters = {
    'frequency': 10,       # Frequency of the simulation in Hertz
    'time': 1,            # Simulated time in seconds
    'delay': 0,  # Delay in number of samples
    'is_closed_loop': True
    }

    # other sets of parameters may be defined if necessary

    # Encapsulate all the parameter dicts
    parameters = {
    'Wavefront': paramsWavefront,
    'Sensor': paramsSensor,
    'Actuator': paramsActuator,
    'Simulation': simulationParameters,
    'Reconstruction': reconstructionParameters
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
    sensor_parameters = parameters['Sensor']
    actuator_parameters = parameters['Actuator']
    reconstruction_parameters = parameters['Reconstruction']

    Nx = sensor_parameters['numPupilx'] # Samples on the x-axis
    Ny = sensor_parameters['numPupily'] # Samples on the y_axis
    lx = sensor_parameters['lx'] # Width of the lenslet array in the x-direction [m]
    ly = sensor_parameters['ly'] # Width of the lenslet array in the y-direction [m]
    
    wf_buffer = []
    intensities_buffer = []
    centroids_buffer = []
    reconstructed_buffer = []
    wf_dm_buffer = []
    
    print("Running closed-loop simulation")

    wfDM = zeros((sensor_parameters['numPupilx'],sensor_parameters['numPupilx']))
    
    delay_buffer = LatencyBuffer(buffer_size, (len(sensor_parameters['lensCentx']), 1))
    
    ## Determine Phi positions                   
    phi_cent_x, phi_cent_y, H = calculate_constants(sensor_parameters, 
                                                    actuator_parameters, 
                                                    reconstruction_parameters)
    
    controller = PIDcontroller(2.0, 0.5, 0)
    # Create grid for in the focal plane
    dx = lx/(Nx - 1.0) # Sample length on x-axis [m]
    dy = ly/(Ny - 1.0) # Sample length on y-axis [m]
    x = arange(0.0, lx + dx, dx) # Sample positions on x-axis [m]
    y = arange(0.0, ly + dy, dy) # Sample positions on y-axis [m]
    
    for i in range(0, iterations):
        print("Running simulation step %d" % (i))
        wf = wfg(sensor_parameters, wavefrontParameters['zernikeModes'],
                 wavefrontParameters['zernikeWeights'])
        wf_buffer.append(wf)
        wf_dm_buffer.append(wfDM)
        
        wfRes = wf - wfDM
        
        xInt, yInt, intensities = wfs(wfRes, sensor_parameters)
        centroids = centroid(intensities, sensor_parameters)
        
        intensities_buffer.append(intensities)
        centroids_buffer.append(centroids)
        
        wfRec = wfr(centroids, sensor_parameters,reconstruction_parameters['geometry'])
        wfRec = delay_buffer.update(wfRec)
        reconstructed_buffer.append(wfRec)
        
        actuator_commands = calculate_actuator_positions(wfRec, H)
        actuator_commands = controller.update(actuator_commands)
        wfDM = calculate_actuated_mirror(actuator_commands, H)
        wfInterp = interpolate.interp2d(phi_cent_x, phi_cent_y, wfDM, kind='cubic')
        wfDM = wfInterp(x, y)

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
    sensor_parameters = parameters['Sensor']
    actuatorParameters = parameters['Actuator']
    simulation_parameters = parameters['Simulation']

    delay_buffer = LatencyBuffer(buffer_size, (sensor_parameters['numPupilx'],
                                     sensor_parameters['numPupilx']))

    
    wf_buffer = []
    intensities_buffer = []
    centroids_buffer = []
    reconstructed_buffer = []
    wf_dm_buffer = []

    print("Running open-loop simulation")
    # The first deformable mirror effect: (No effect)
    wfDM = dm(0, sensorParameters, actuatorParameters)

    for i in range(0, iterations):
        print("Running simulation step %d" % (i))
        wf = wfg(sensorParameters, wavefrontParameters['zernikeModes'],
                 wavefrontParameters['zernikeWeights'])
        wfRes = wf - wfDM
        xInt, yInt, intensities = wfs(wfRes, sensorParameters)
        centroids = centroid(intensities, sensorParameters)
        wfRec = wfr(centroids, sensorParameters,simulation_parameters['geometry'])
        wfRec = delay_buffer.update(wfRec)
        wfDM = dm(0, sensorParameters, actuatorParameters)

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


def calculate_constants(sensor_parameters, actuator_parameters,
                        reconstruction_parameters):
    lens_centers_x = sensor_parameters['lensCentx']
    lens_centers_y = sensor_parameters['lensCenty']
    length_x = sensor_parameters['lx']
    length_y = sensor_parameters['ly']
    n_apertures_x = sensor_parameters['noApertx']
    n_apertures_y = sensor_parameters['noAperty']
    dl = sensor_parameters['dl']
    D = sensor_parameters['D']
    geometry = reconstruction_parameters['geometry']
    sig1_mult = actuator_parameters['sig1_multiplier']
    sig2_mult = actuator_parameters['sig2_multiplier']
    w1 = actuator_parameters['w1']
    w2 = actuator_parameters['w2']
    
    
    phi_cent_x, phi_cent_y =  determine_phi_positions(lens_centers_x, length_x, n_apertures_x,
                                                      lens_centers_y, length_y, n_apertures_y,
                                                      dl, D, geometry)
    
    phi_centers = array([phi_cent_x, phi_cent_y])
    phi_centers = phi_centers.T
    
    actuator_positions_x = lens_centers_x * length_x
    actuator_positions_y = lens_centers_y * length_y
    actuator_positions = array([actuator_positions_x, 
                               actuator_positions_y])
    actuator_positions = actuator_positions.T
    
    nwfRec = len(phi_cent_x)
    numAct = len(lens_centers_x)
    sig1 = sig1_mult * dl
    sig2 = sig2_mult * dl
    H = calculateH(nwfRec, numAct, phi_centers, actuator_positions, sig1, sig2, w1, w2)
    return phi_cent_x, phi_cent_y, H

    
def run_simulation(parameters):
    """ Runs the configured simulation. Either an open or closed loop.

    """
    simulation_parameters = parameters['Simulation']
    iterations = int(simulation_parameters['frequency'] *
                  simulation_parameters['time'])

    delay_buffer_size = simulation_parameters['delay'] + 1

    if simulation_parameters['is_closed_loop']:
        results = runClosedLoop(parameters, iterations, delay_buffer_size)
    else:
        results = runOpenLoop(parameters, iterations, delay_buffer_size)
    plot_simulation(results, iterations, parameters)


def plot_simulation(results, iterations, parameters):
    sensor_parameters = parameters['Sensor']

    Nx = sensor_parameters['numPupilx'] # Samples on the x-axis
    Ny = sensor_parameters['numPupily'] # Samples on the y_axis
    lx = sensor_parameters['lx'] # Width of the lenslet array in the x-direction [m]
    ly = sensor_parameters['ly'] # Width of the lenslet array in the y-direction [m]
    
            # Create grid for in the focal plane
    dx = lx/(Nx - 1.0) # Sample length on x-axis [m]
    dy = ly/(Ny - 1.0) # Sample length on y-axis [m]
    x = arange(0.0, lx + dx, dx) # Sample positions on x-axis [m]
    y = arange(0.0, ly + dy, dy) # Sample positions on y-axis [m]
    
    wf = results['wf']
    wfDm = results['wf_dm']

    pl.figure()
    pl.ion()
    pl.show()
    wf_plot = pl.pcolormesh(x,y,wf[0] - wfDm[0], vmin=-0.0035, vmax=0.0035)
    pl.xlabel('x (mm)')
    pl.ylabel('y (mm)')
    pl.title('Deformed wave-front')
    pl.savefig('wfRes000.png')
    for i in range(1, iterations):
        wf_res = wf[i] - wfDm[i]
        wf_plot.set_array(wf_res.ravel())
        pl.draw()
        pl.savefig('wfRes' + str(i).zfill(3) + '.png')
        time.sleep(1)
        
    
    
parameters = setup_params()
run_simulation(parameters)
