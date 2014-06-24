from numpy import *
from scipy import *
from zernike import *
from phaseScreen import *

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

def wfg(params, wavefrontParams,debug = False):
    waveFrontPhi = numpy.zeros((params['numPupilx'],params['numPupily']))
    
    #Zernike
    if 'zernike' in wavefrontParams:
        zernikeModes = wavefrontParams['zernike']['zernikeModes']
        zernikeWeights = wavefrontParams['zernike']['zernikeWeights']
        
        zw = ZernikeWave()
	zw.addMode(zernikeModes, zernikeWeights)
	waveFrontPhi = waveFrontPhi + zw.createWavefront(params['numPupilx'],params['numPupily'])
        
        if debug:
	   zw.plotWavefront(params['numPupilx'],params['numPupily'])
    
    if 'kolmogorov' in wavefrontParams:
        phaseScreenParams = wavefrontParams['kolmogorov']
        ps = PhaseScreen()
        ps.setType('Kolmogorov')
        ps.setParams(phaseScreenParams)
        waveFrontPhi = waveFrontPhi + ps.createWavefront(params['numPupilx'],params['numPupily'])
        
        if debug:
	   ps.plotWavefront(params['numPupilx'],params['numPupily'])

    if 'vonkarman' in wavefrontParams:
        phaseScreenParams = wavefrontParams['vonkarman']
        ps = PhaseScreen()
        ps.setType('vonKarman')
        ps.setParams(phaseScreenParams)
        waveFrontPhi = waveFrontPhi + ps.createWavefront(params['numPupilx'],params['numPupily'])
        
        if debug:
	   ps.plotWavefront(params['numPupilx'],params['numPupily'])
        				
    return waveFrontPhi