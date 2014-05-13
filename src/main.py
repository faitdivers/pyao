# Main file for PyAO toolbox
# _  _  _  _         _  _  _        _  _  _  _        _  _  _       
#(_)(_)(_)(_)     _ (_)(_)(_) _   _(_)(_)(_)(_)_   _ (_)(_)(_) _    
# (_)      (_)_  (_)         (_) (_)          (_) (_)         (_)   
# (_)        (_) (_)             (_)_  _  _  _    (_)               
# (_)        (_) (_)               (_)(_)(_)(_)_  (_)               
# (_)       _(_) (_)          _   _           (_) (_)          _    
# (_)_  _  (_)   (_) _  _  _ (_) (_)_  _  _  _(_) (_) _  _  _ (_)   
#(_)(_)(_)(_)       (_)(_)(_)      (_)(_)(_)(_)      (_)(_)(_)   
#

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

#-----------------------------------------------------------------------
#
#
#-----------------------------------------------------------------------
def runClosedLoop(iterations):
	paramsSensor, paramsActuator = setup_params()
	for i in range(0, iterations):
		print "Running simulation step %d" % (i)
		wf = wfg(paramsSensor)
		intensities = wfs(wf) 
		centroids = centroid(intensities, paramsSensor)
		wfRec = wfr(centroids, paramsSensor)
		actCommands = control(wfRec, paramsActuator)
		wfDM = dm(actCommands, paramsSensor)
		wfRes = wf-wfDM
	return
		
def runOpenLoop():
	paramsSensor, paramsActuator = setup_params()
	print "Running open loop simulation"
	# Generate wavefront
	wf = wfg(paramsSensor)
	#pl.imshow(wf), pl.show(), pl.title('Incoming wavefront')

	# Generate intensity measurements
	intensities = wfs(wf)
	
	# Compute centroids (this step is not needed if we are to use focal 
	# plane reconstruction techniques) 
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
	return

#runClosedLoop(10)

runOpenLoop()
