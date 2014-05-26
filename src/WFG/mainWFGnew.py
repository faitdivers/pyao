from numpy import *
from scipy import *
from zernike import *

# Create a wavefront, comprising of a sum of zernike modes, with their respective weithings.
# Syntax:
# 	wfg(params, zernikeModes, zernikeWeights):
# 	wfg(params, zernikeModes, zernikeWeights, debug):
#	params: 	an array specifiying the discretization of the grid.
#	zernikeModes:	a scalar or array of the zernike modes in the wavefront.
#	zernikeWeights: a scalar or array of the zernike weights, the position in the array matches to the position of the specified mode in the zernikeModes array.	
#	debug:		specify True if you wish to plot the wavefront
#	
# The function creates a wavefront built by the modes and weights specified in the zernikeModes and
# zernikeWeights parameters. In params, the parameters 'numImagx' and 'numImagy' must be specified
# in order to make a discretization of the wavefront. Further the parameter debug can be specified
# if a plot of the constructed wavefront is desired. 

def wfg(params, zernikeModes, zernikeWeights, debug=False):
	zw = ZernikeWave()
	zw.addMode(zernikeModes, zernikeWeights)
	waveFrontPhi = zw.createWavefront(params['numImagx'],params['numImagy'])
	
	# When calling with debug = true, plot the created wavefront if desired, so you can see what is done.
	if debug:
		zw.plotWavefront(paramt['numImagx'],paramt['numImagy'])

	return waveFrontPhi
