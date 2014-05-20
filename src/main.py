# Main file for PyAO toolbox

from numpy import *
import matplotlib.pyplot as pl

from WFG.mainWFG import * 
from WFS.mainWFS import * 
from Centroid.mainCentroid import * 
from WFR.mainWFR import * 
from Control.mainControl import * 
from DM.mainDM import * 


# --------------------------------------------------
# Setting up the parameters
def setup_params():
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
	'F': 18e-3,      # Focal length [m]
	'Diam': 300e-6, 	# Diameter of pupil [m] - is this of lenslet or system?
	'lam': 630e-9, 	# Wavelength [m] 
	'Lx': 4000e-6,   # Support Width in x dimension (real space) [m]
	'Ly': 4000e-6,   # Support Width in y dimension (real space) [m]
	}
	paramsActuator = {
	# number of actuators
	'numActx' : 8,
	'numActy' : 8,
	# parameters to characterize influence function
	# ...
	}

	# other sets of parameters may be defined if necessary

	return paramsSensor, paramsActuator

# --------------------------------------------------

paramsSensor, paramsActuator = setup_params()

print paramsSensor['numPupilx']

# NOTE: this is an open-loop simulation; bear in mind that the end goal is to run it in closed 
# loop with changing wavefronts

# Generate wavefront
wf = wfg(paramsSensor)
#pl.imshow(wf), pl.show(), pl.title('Incoming wavefront')

# Generate intensity measurements
intensities = wfs(wf, paramsSensor) 

# Compute centroids (this step is not needed if we are to use focal plane reconstruction techniques)
centroids = centroid(intensities, paramsSensor)
#print centroids.shape

# Reconstruct the wavefront
wfRec = wfr(centroids, paramsSensor)

# Compute the actuator commands via a control technique
actCommands = control(wfRec, paramsActuator)

# Deformable mirror
wfDM = dm(actCommands, paramsSensor)

# Compute the residual wavefront
wfRes = wf-wfDM

# Plot the results



