'''
Created on May 22, 2014

@author: forcaeluz
'''
#from collections import deque
import numpy as np
import operator as op

class LatencyBuffer():
    
    def __init__(self, bufferLength, data_shape):
        self.data_shape = data_shape
        self.data_framesize = reduce(op.mul, data_shape)
        self.data = np.zeros(bufferLength * self.data_framesize)
        self.index = 0
       
    def update(self, data):
        self._set_newest(data)
        return self._get_oldest()
    
    def _get_oldest(self):
        r_index = (self.index + np.arange(self.data_framesize)) % self.data.size
        output = self.data[r_index]
        return output
    
    def _set_newest(self, data):
        if data.shape == self.data_shape:
            x_index = (self.index + np.arange(data.size)) % self.data.size
            self.data[x_index] = data
            self.index = x_index[-1] + 1    
        else:
            print("ERROR: Data shape is not correct")
        
    def get_stored_data(self):
        return self.data
