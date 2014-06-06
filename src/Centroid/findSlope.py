# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 20:21:00 2014

@author: Herminarto
"""

def findSlope(Centroid,idealCenter,f):
    # f is the distance between the aperture array and the detector array.
    # delta is the error between centroid and ideal spot    
    delta = Centroid-idealCenter
    
    # Slope calculation
    slope =  [z/f for z in delta]   
    
    return slope