# -*- coding: utf-8 -*-
"""
Created on Wed May 21 17:11:14 2014

@author: Herminarto
"""

from numpy import *

# so far only for single lens

def centroid(intensities, params):
    # parameters for centroid:
    threshold = 0.1
    # f is the distance between the aperture array and the detector array.
    # I think this f should be inside params
    # define f=18e-3 just for testing
    f = 18e-3
    # I think this idealcenter should be inside params
    # define idealCenter = (25,25) just for testing    
    idealCenter = (25,25)
    
    maxintensity = intensities.max()
    trshld = maxintensity*threshold
    
    # call function to calculate the centroid
    centroid = findCentroid(intensities,trshld)
    
    # call function to calculate the slope
    slope = findSlope(centroid,idealCenter,f)
    
    ans = (centroid,slope)
	
    return ans
