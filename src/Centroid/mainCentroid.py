# -*- coding: utf-8 -*-
"""
Created on Sun Jun 01 23:25:26 2014

@author: Herminarto
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as pl

from findCentroid import *
from findSlope import *

#from WFG.mainWFG import *
#from WFS.mainWFS import *
#from Centroid.mainCentroid import *
#from WFR.mainWFR import *
#from Control.mainControl import *
#from DM.mainDM import *

# Calculate the centroids of an intensity distribution yielded by Shack-Hartmann  
# wavefront sensor.
# Given the priory knowledge of the number of lenslet/apertures and the ideal
# spot position.

def centroid(intensities, paramsSensor):
    # parameters for centroid:
    threshold = 0.1
    # Unwrap paramsSensor
    Nx = paramsSensor['Nx'] # Samples on the x-axis per lenslet
    Ny = paramsSensor['Ny'] # Samples on the y_axis per lenslet
    lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
    ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
    lensCentx = paramsSensor['lensCentx'] # Lenslet centers on x-axis [m]
    lensCenty = paramsSensor['lensCenty'] # Lenslet centers on y-axis [m]
    f = paramsSensor['f'] # Focal length [m]
    
    # defining the threshold for centroid algorithm method
    maxintensity = intensities.max()
    trshld = maxintensity*threshold
    
    # number of pixel in image:
    pixX = intensities.shape[1]     # number of pixel in x direction
    pixY = intensities.shape[0]     # number of pixel in y direction
    
    # pixel size:
    x = lx/pixX                     # pixel size in x direction
    y = ly/pixY                     # pixel size in y direction

    # width of the region for 1 aperture
    wx = 0.5*(lensCentx[2]-lensCentx[1])/x # distance between centroid to edge of region of each aperture
    wy = 0.5*(lensCenty[2]-lensCenty[1])/y # distance between centroid to edge of region of each aperture

    # ideal centroid spot in pixel
    pixlensCentx = [z/x for z in lensCentx]
    pixlensCenty = [z/y for z in lensCenty]
    idealCenter = [pixlensCentx,pixlensCenty]     # make a vector of pixlensCentx and pixlensCenty
    idealCenter = np.asarray(idealCenter)
    idealCenter = idealCenter.reshape((2,Nx))
    
    # To calculate the centroid for each apertures, we need to calculate the intensities
    # within a specified region of interest. To do so, we should create mask matrix
    # which has value 1 at those region of interest and 0 otherwise.
    # The mask matrix then multiplied with the intencities matrix, results in
    # a new matrix which only has intensity value in the region of interest.    
    
    # initialize the matrix mask
    mask = zeros((len(intensities),len(intensities)))
    
    # initialize the array of matrix mask
    maskmatrix = np.empty([0,len(intensities)])
    
    # crating matix mask
    for a in range(len(lensCentx)):
        centX = pixlensCentx[a]     # ideal centroid x coordinate
        beginx = int(centX-wx)      # begining of the region of interest in x-axis
        endx = int(centX+wx)        # end of the region of interest in x-axis
        
        centY = pixlensCenty[a]     # ideal centroid y coordinate
        beginy = int(centY-wx)      # begining of the region of interest in y-axis
        endy = int(centY+wx)        # end of the region of interest in y-axis
        
        for i in range(len(intensities)):
            for j in range(len(intensities)):
                for k in range(beginy,endy):
                    for m in range(beginx,endx):
                        mask[k][m]=1    # creating 1 as value for mask
                        
        maskmatrix = np.append(maskmatrix, mask, axis=0)    # merge the current mask with previous mask
        mask = zeros((len(intensities),len(intensities)))    # reset the mask

    # Then we calculate the centroids and slopes.
    # The centroids and slopes are represented as a vector consisting every
    # centroid and slope for each apertures.   
    
    # initialize the centroidvector and slopevector
    centroidvector = zeros((Nx,2))
    slopevector = zeros((Nx,2))
    
    # doing iteration to calculate centroid for each apertures
    for h in range(Nx):
        maskh = maskmatrix[range(int(len(intensities)*h),int(len(intensities)*(h+1))),0:len(intensities)]
        # defining which internsity is calculated
        intensityComp = intensities*maskh
        # calculating centroid
        centroid = findCentroid(intensityComp,trshld)
        centroidvector[h] = centroid
             
    centroidvector = np.transpose(centroidvector)
    # Calculating the slope vector:
    slopevector = findSlope(centroidvector,idealCenter,f)
        
    # the output of centroid function is a vector of centroids and slopes
    # in the form of :
    # [s_x(0,0),.,s_x(0,N),.,s_x(M,0),.,s_x(M,N),s_y(0,0),.,s_y(0,N),.,s_y(M,0),.,s_y(M,N)]^T
    # to do that we have to reshape the matrix slopevector and centroidvector
    
    slopevector = zip(*slopevector)
    slopevector = np.asarray(slopevector)
    slopevector = np.transpose(slopevector)
    slopevector = slopevector.reshape((1,2*Nx))
    
    centroidvector = zip(*centroidvector)
    centroidvector = np.asarray(centroidvector)
    centroidvector = np.transpose(centroidvector)
    centroidvector = centroidvector.reshape((1,2*Nx))
    
    ans = slopevector
	
    return ans
