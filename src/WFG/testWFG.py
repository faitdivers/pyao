from mainWFG import * 

def setup_params() :
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
	return paramsSensor,paramsActuator
	
params,paramsAct = setup_params()	
count = 0
print "Check properties:"
for obj in params :
    print "\tprop(%d) | %r = %d" %(count,obj,params[obj])
    count += 1
    
res = wfg(params)
print "\nWave Front Generation:"
print "%r" %res
