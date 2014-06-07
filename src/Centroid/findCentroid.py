# -*- coding: utf-8 -*-
"""
Created on Wed May 21 17:11:14 2014

@author: Herminarto
"""

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