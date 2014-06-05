# -*- coding: utf-8 -*-
"""
Created on Sun Jun 01 23:25:26 2014

@author: Herminarto
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as pl

from WFG.mainWFG import *
from WFS.mainWFS import *
from Centroid.mainCentroid import *
from WFR.mainWFR import *
from Control.mainControl import *
from DM.mainDM import *

# Calculate the centroids of an intensity distribution yielded by Shack-Hartmann  
# wavefront sensor.
# Given the priory knowledge of the number of lenslet/apertures and the ideal
# spot position.

def centroid(intensities, params):
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
    D = paramsSensor['D'] # Lens diameter [m]
    noApertyx = paramsSensor['noApertyx']
    noApertyy = paramsSensor['noApertyy']
    
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
    pixlensCentx = lensCentx/x
    pixlensCenty = lensCenty/y 
    idealCenter = pixlensCentx,pixlensCenty     # make a vector of pixlensCentx and pixlensCenty
  
    # To calculate the centroid for each apertures, we need to calculate the intensities
    # within a specified region of interest. To do so, we should create mask matrix
    # which has value 1 at those region of interest and 0 otherwise.
    # The mask matrix then multiplied with the intencities matrix, results in
    # a new matrix which only has intensity value in the region of interest.    
    
    # initialize the matrix mask
    mask = zeros((len(intensities),len(intensities))
    # initialize the array of matrix mask
    mask_matrix = np.empty(shape=[0,len(intensities)]) 
    
    # crating matix mask
    for a in range(len(lensCentx)):
        b = pixlensCentx[a]
        begin = int(b-wx)
        end = int(b+wx) 
        
        c = pixlensCenty[a]
        beginy = int(b-wy)
        endy = int(b+wy) 
        
        for i in range(len(intensities)):
            for j in range(len(intensities)):
                for k in range(beginy,endy):
                    for m in range(begin,end):
                        mask[k][m]=1
                        
        mask_matrix = np.append(mask_matrix, mask, axis=0) 
        mask = zeros((len(intensities),len(intensities))

    # Then we calculate the centroids and slopes.
    # The centroids and slopes are represented as a vector consisting every
    # centroid and slope for each apertures.   
    
    # initialize the centroidvector and slopevector
    centroidvector = zeros((Nx,2))
    slopevector = zeros((Nx,2))
    
    # doing iteration to calculate centroid for each apertures
    for h in range(Nx):
        maskh = matrixMask[range(int(Nx*h),int(Nx*(h+1))),0:Nx]
        # defining which internsity is calculated
        intensityComp = intensities*maskh
        # calculating centroid
        centroid = findCentroid(intensityComp,trshld)
        # calculating slope
        slope = findSlope(centroid,idealCenter,f)
        centroidvector[h] = centroid
        slopevector[h] = slope
    
    # the output of centroid function is a vector of centroids and slopes
    # in the form of :
    # [s_x(0,0),.,s_x(0,N),.,s_x(M,0),.,s_x(M,N),s_y(0,0),.,s_y(0,N),.,s_y(M,0),.,s_y(M,N)]^T
    # to do that we have to reshape the matrix slopevector and centroidvector
    
    slopevector = zip(*slopevector)
    centroidvector = zip(*centroidvector)
    ans = slopevector
	
    return ans
    
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
    Centroid = (float(Mx)/Sum,float(My)/Sum)
    
    # return of function
    return Centroid
    
    
def findSlope(Centroid,idealCenter,f):
    # f is the distance between the aperture array and the detector array.
    deltax = Centroid[0]-idealCenter[0]
    deltay = Centroid[1]-idealCenter[1]
    
    # wavefront slope x and y coordinates:
    slopex = deltax/f
    slopey = deltay/f
    
    slope = (slopex,slopey)
    
    return slope
