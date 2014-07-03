# -*- coding: utf-8 -*-
"""
Created on Sun Jun 01 23:25:26 2014

@author: Herminarto
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as pl

# Calculate the centroids of an intensity distribution yielded by Shack-Hartmann wavefront sensor.
# Given the priory knowledge of the number of lenslet/apertures and the ideal spot position.

def centroid(intensities, paramsSensor):
    # parameters for centroid:
    threshold = paramsSensor['illumThreshold']
    
    # Unwrap paramsSensor
    lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
    ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
    lensCentx = paramsSensor['lensCentx']*lx; # Lenslet centers on x-axis [m]
    lensCenty = paramsSensor['lensCenty']*ly; # Lenslet centers on y-axis [m]
    f = paramsSensor['f'] # Focal length [m]
    noApertx = paramsSensor['noApertx'] # number of apertures in x axis
    noAperty = paramsSensor['noAperty'] # number of apertures in y axis
    numImagx = paramsSensor['numImagx'] # Samples on the x-axis per lenslet
    numImagy = paramsSensor['numImagy'] # Samples on the y_axis per lenslet
    
    # defining the threshold for centroid algorithm method
    maxintensity = intensities.max()
    trshld = maxintensity*threshold
      
    # pixel size
    dx = lx/numImagx                      # pixel size in x direction
    dy = ly/numImagy                      # pixel size in y direction

    # ideal centroid spot in pixel
    pixlensCentx = [(round(z/dx)-1) for z in lensCentx] # round() is used because in pixel, -1 used as the index in python starts at 0
    pixlensCenty = [(round(z/dy)-1) for z in lensCenty] # round() is used because in pixel, -1 used as the index in python starts at 0
    idealCenter = [pixlensCentx,pixlensCenty]           # make a vector of pixlensCentx and pixlensCenty
    idealCenter = np.asarray(idealCenter)
    idealCenter = idealCenter.reshape((2,noApertx*noAperty))
      
    # initialize the centroidvector
    centroidvector = zeros((len(pixlensCentx),2))
    
    noApertures =  int(len(idealCenter[0])) 
    
    # Finding the width of region of interest
    # With the assumsion distance between center to its nearest center are all same
    # If function is used to distinguish whether the center is on the edge of the geometry
    if (pixlensCentx[2]-pixlensCentx[1])==(pixlensCentx[3]-pixlensCentx[2]):
        widthx = int(pixlensCentx[2]-pixlensCentx[1])
    else:
        widthx = int(pixlensCentx[4]-pixlensCentx[3])
    # The centroid of each aperture will be calculated individually based on region of interest.
    # The region of interest of matrix intensities is determined in a loop process.
    
    widthy = int(pixlensCenty[1+noApertx]-pixlensCenty[1])
    
    # The iteration for center in each aperture
    for k in range(noApertures):
        # Region of Interest:
        
        xbegin = int(pixlensCentx[k]-(widthx/2)+1)
        if (xbegin < 0):
            xbegin = 0;
        
        xend = int(pixlensCentx[k]+(widthx/2)+1)
        if (xend > numImagx-1):
            xend = numImagx-1;

        ybegin = int(pixlensCenty[k]-(widthy/2)+1)
        if (ybegin < 0):
            ybegin = 0;
        
        yend = int(pixlensCenty[k]+(widthy/2)+1)
        if (yend > numImagy-1):
            yend = numImagy-1;

        # Matrix of Interest
        IntensitiesofInterst = intensities[range(int(xbegin),int(xend)),ybegin:yend]
        # Calculating centroid
        centroid = findCentroid(IntensitiesofInterst,trshld)
        centroid[0]=centroid[0]+xbegin
        centroid[1]=centroid[1]+ybegin
        centroidvector[k] = centroid
    
    # Transpose of centroidvector to make the dimension same as idealCenter matrix
    centroidvector = np.transpose(centroidvector)
    # Calculating the slope vector:
    slopevector = findSlope(centroidvector,idealCenter,f)
            
    # The output of centroid function is a vector of centroids and slopes in the form of :
    # [s_x(0,0),.,s_x(0,N),.,s_x(M,0),.,s_x(M,N),s_y(0,0),.,s_y(0,N),.,s_y(M,0),.,s_y(M,N)]
    # to do that we have to reshape the matrix slopevector and centroidvector
    slopevector = zip(*slopevector)
    slopevector = np.asarray(slopevector)
    slopevector = np.transpose(slopevector)
    slopevector = slopevector.reshape((2*noApertx*noAperty,1))
            
    return slopevector  

def findCentroid(matrix,trshld):
    # Initialization
    Mx  = 0
    My  = 0
    Sum = 0
    
    # Looking at the value for each pixel coordinate
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]>=trshld:
                # Calculate the sum of each value from every pixel
                Mx  += j
                My  += i
                # Calculate total pixel
                Sum += 1
                
    # Compute the centroid using mean    
    Centroid = ([Mx/Sum,My/Sum])
    
    # return of function
    return Centroid
   
def findSlope(Centroid,idealCenter,f):
    # f is the distance between the aperture array and the detector array.
    # delta is the error between centroid and ideal spot    
    delta = Centroid-idealCenter
    
    # Slope calculation
    slope =  [z/f for z in delta]   
    
    return slope

