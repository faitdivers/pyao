# -*- coding: utf-8 -*-
"""
Created on Wed May 21 14:17:03 2014

@author: Herminarto
"""

def findAVG(matrix):
    import pylab
    grid = pylab.array(matrix)
    avg = ( pylab.average(pylab.array(grid.nonzero())[1,:]), pylab.average(pylab.array(grid.nonzero())[0,:]) )
    return avg