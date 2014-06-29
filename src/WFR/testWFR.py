from mainWFR import *
from plotWavefront import *
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
from WFS.lensArrayConfig import *
from WFG.mainWFG import *
from WFS.mainWFS import *
from Centroid.mainCentroid import *
import matplotlib.pyplot as plt
import time

def setup_params():
	""" Set-up the simulation parameters

	Returns:
		Multiple dicts, containing the parameters and their values.
	"""

	paramsWavefront = {
    # Scalar or array containing the zernike modes
    'zernikeModes': [4],
    # Scalar or array containing the zernike weights, with respect to the modes
    'zernikeWeights': [1.0]
    }

	paramsSensor = {
	# number of samples in the pupil plane
	'numPupilx' : 200,
	'numPupily' : 200,
	# number of samples in the imaging plane(s)
	'numImagx' : 200,
	'numImagy' : 200,
	# number of apertures in the wfs
	'noApertx': 5,
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
	}
	
	# Compute lenslet centres and check minimal array widths 
	lx, ly, lensCentx, lensCenty = lensletCentres(paramsSensor)
	# Normalized lenslet centers
	paramsSensor['lensCentx'] = lensCentx
	paramsSensor['lensCenty'] = lensCenty
	# Set correct array widths
	paramsSensor['lx'] = lx
	paramsSensor['ly'] = ly
	
	# Encapsulate all the parameter dicts
	parameters = {
	'Sensor' : paramsSensor,
	'Wavefront' : paramsWavefront
	}

	return parameters

def test_run():
	# Get parameters.
	parameters = setup_params()
	sensorParameters = parameters['Sensor'];
	wavefrontParameters = parameters['Wavefront'];

	# Tilt in the x direction
	# centroids_ones = 0.*ones((sensorParameters['noApertx']*sensorParameters['noAperty'],1))
	# centroids_zeros = 1.0*ones((sensorParameters['noApertx']*sensorParameters['noAperty'],1))
	# centroids = concatenate([centroids_ones, centroids_zeros])
	# #centroids = ones((sensorParameters['noApertx']*sensorParameters['noAperty']*2,1))
	# wfRecTilt,phiCentersX, phiCentersY = wfr(centroids, sensorParameters)
	# plotWavefront(phiCentersX,phiCentersY,wfRecTilt)

	# Zernike aberration
	wf = wfg(sensorParameters, wavefrontParameters['zernikeModes'], wavefrontParameters['zernikeWeights'])
	xInt, yInt, intensities = wfs(wf, sensorParameters)
	plt.imshow(intensities)
	print intensities
	time.sleep(1000)
	centroids = centroid(intensities, sensorParameters)
	wfRecZer,phiCentersX, phiCentersY = wfr(centroids, sensorParameters)
	plotWavefront(phiCentersX,phiCentersY,wfRecZer)

	return

test_run()
