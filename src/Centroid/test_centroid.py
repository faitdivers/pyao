# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 23:00:47 2014

@author: Herminarto
"""
from mainCentroid import *
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')

from WFS.lensArrayConfig import *

def setup_params():
        
    paramsSensor = {
    # number of samples in the pupil plane
    'numPupilx' : 100, # Not used in WFS
    'numPupily' : 100, # Not used in WFS
    # number of samples in the imaging plane(s)
    'numImagx' : 100, # Not used in WFS
    'numImagy' : 100, # Not used in WFS
    # number of apertures in the wfs
    'noApertx': 5, # Not used in WFS
    'noAperty': 5, # Not used in WFS
    # Number of samples of the incoming phase
    'Nx' : 20,
    'Ny' : 20,
    # Focal Length [m]
    'f' : 18.0e-3,
    # Diameter of aperture of single lenslet [m]
    'D' : 300.0e-6,
    # Wavelength [m]
    'lam' : 630.0e-9,
    # Width of the lenslet array [m]
    'lx' : 1.54e-3,
    'ly' : 1.54e-3,
    # Distance between lenslets [m] 
    'dl' : 10.0e-6, 
    # Support factor used for support size [m] = support factor x diameter lenslet
    'supportFactor' : 4,
    }

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
    }
    
    return parameters
    
def test_centroid():
    # Get parameters.
    parameters = setup_params()
    sensorParameters = parameters['Sensor'];
    
    intensities = ones((100,100))
    centroids = centroid(intensities, sensorParameters)
    return centroids
 
slopevector = test_centroid()

