# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 20:21:00 2014

@author: Herminarto
"""

def findSlope(Centroid,idealCenter,f):
    # f is the distance between the aperture array and the detector array.
    deltax = Centroid[0]-idealCenter[0]
    deltay = Centroid[1]-idealCenter[1]
    
    # wavefront slope x and y coordinates:
    slopex = deltax/f
    slopey = deltay/f
    
    slope = (slopex,slopey)
    
    return slope