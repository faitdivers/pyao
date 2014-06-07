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
    threshold = 0.3
    
    # Unwrap paramsSensor
    lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
    ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
    lensCentx = paramsSensor['lensCentx'] # Lenslet centers on x-axis [m]
    lensCenty = paramsSensor['lensCenty'] # Lenslet centers on y-axis [m]
    f = paramsSensor['f'] # Focal length [m]
    noApertx = paramsSensor['noApertx'] # number of apertures in x axis
    noAperty = paramsSensor['noAperty'] # number of apertures in y axis
    Nx = paramsSensor['Nx'] # Samples on the x-axis per lenslet
    Ny = paramsSensor['Ny'] # Samples on the y_axis per lenslet
    
    # defining the threshold for centroid algorithm method
    maxintensity = intensities.max()
    trshld = maxintensity*threshold
      
    # pixel size
    # (Nx*noApertx) and (Ny*noAperty) = number of pixel for the whole image in x and y direction respt.
    dx = lx/(Nx*noApertx)                       # pixel size in x direction
    dy = ly/(Ny*noAperty)                       # pixel size in y direction

    # ideal centroid spot in pixel
    pixlensCentx = [round(z/dx) for z in lensCentx] # round() is used because in pixel
    pixlensCenty = [round(z/dy) for z in lensCenty] # round() is used because in pixel
    idealCenter = [pixlensCentx,pixlensCenty]     # make a vector of pixlensCentx and pixlensCenty
    idealCenter = np.asarray(idealCenter)
    idealCenter = idealCenter.reshape((2,noApertx*noAperty))
    
    # The centroid of each aperture will be calculated individually based on region of interest.
    # The region of interest of matrix intensities is determined in a loop process.    
    
    # initialize the centroidvector
    centroidvector = zeros((noApertx*noAperty,2))
    # Loop process for defining region of interest and calculating centroid
    for q in range(noAperty): 
        for r in range(noApertx):
            IntensitiesofInterst = intensities[range((Ny*q),(Ny*(q+1))),(r*Nx):(Nx*(r+1))]
            #IntensitiesofInterst = np.asarray(IntensitiesofInterst)
            centroid = findCentroid(IntensitiesofInterst,trshld)
            centroid[0]=centroid[0]+r*Nx
            centroid[1]=centroid[1]+q*Ny
            centroidvector[(q*noAperty)+r] = centroid
    
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
    slopevector = slopevector.reshape((1,2*noApertx*noAperty))
	
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
    Centroid = ([float(Mx)/Sum,float(My)/Sum])
    
    # return of function
    return Centroid
   
def findSlope(Centroid,idealCenter,f):
    # f is the distance between the aperture array and the detector array.
    # delta is the error between centroid and ideal spot    
    delta = Centroid-idealCenter
    
    # Slope calculation
    slope =  [z/f for z in delta]   
    
    return slope
    ans = slopevector
	
    return ans