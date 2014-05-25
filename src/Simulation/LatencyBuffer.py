'''
Created on May 22, 2014

@author: forcaeluz
'''
import numpy as np
import operator as op


class LatencyBuffer():
    """ LatencyBuffer class: A ring buffer to simulate latency
        The LatencyBuffer is a ring-buffer created to introduce
        a latency into the simulation.
    """
    def __init__(self, bufferLength, data_shape):
        """ Constructs the LatencyBuffer

            The constructor pre-allocate the whole buffer, initializes it to 0
            and set the write index to 0.

        Args:
            bufferLenght: Number of data-frames that the buffer should store.
            data_shape: Size of the data coming in multiple dimensions.
                Example: (10, 1) is a vector of 10 elements
                         (10, 10) is a 10x10 matrix
                         (10, 10, 10) is a 10x10x10 3D matrix
        """
        self.data_shape = data_shape
        self.data_framesize = reduce(op.mul, data_shape)
        self.data = np.zeros(bufferLength * self.data_framesize)
        self.index = 0

    def update(self, data):
        """ Updates the content of the buffer.

        First the new data is stored into the buffer, after that the buffer
        is read.

        Args:
            data: The data to be inserted into the buffer.

        Returns:
            The oldest stored data.

        TODO:
            - Better error handling
        """
        self._set_newest(data)
        return self._get_oldest()

    def _get_oldest(self):
        """ Returns the oldest data stored

        """
        r_index = (self.index + np.arange(self.data_framesize))
        r_index = r_index % self.data.size
        output = self.data[r_index]
        output = np.reshape(output, self.data_shape)
        return output

    def _set_newest(self, data):
        """ Set the data that should be stored in the buffer at write index

        TODO:
            - Better error handling.
        """
        if data.shape == self.data_shape:
            x_index = (self.index + np.arange(data.size)) % self.data.size
            self.data[x_index] = data
            self.index = x_index[-1] + 1
        else:
            print("ERROR: Data shape is not correct")

    def get_stored_data(self):
        """ Returns all the content of the buffer.

        """
        return self.data
