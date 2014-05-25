'''
Created on May 24, 2014

@author: forcaeluz
'''
import unittest
import LatencyBuffer
import numpy as np


class LatencyBufferTest(unittest.TestCase):

    def test_constructor_datasize(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(10, dataSize)
        data = myBuffer.get_stored_data()
        data_size = len(data)
        self.assertEqual(1000, data_size)

    def test_constructor_emptydata(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(10, dataSize)
        data = myBuffer.get_stored_data()
        result = all(x == 0 for x in data)
        self.assertTrue(result, "Not all the elements are zeros")

    def test_update_data(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(10, dataSize)
        dataSet = np.ones([10, 10])
        myBuffer.update(dataSet)
        data = myBuffer.get_stored_data()
        result1 = all(x == 1 for x in data[range(100)])
        result2 = all(x == 0 for x in data[range(100, 1000)])
        self.assertTrue(result1, "Not all the first 100 elements are ones")
        self.assertTrue(result2, "Not all the last 900 elements are zeros")

    def test_update_return(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(2, dataSize)
        dataSet = np.ones([10, 10])
        data = myBuffer.update(dataSet)
        result1 = all(x == 0 for x in data)
        self.assertTrue(result1, "Not all the first 100 elements are ones")

    def test_udate_return_2steps(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(2, dataSize)
        dataSet1 = np.ones([10, 10])
        myBuffer.update(dataSet1)
        dataSet2 = 2 * np.ones([10, 10])
        actual = myBuffer.update(dataSet2)
        result = all(x == 1 for x in actual)
        self.assertTrue(result, "Not all the first 100 elements are ones")

    def test_udate_return_3steps(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(2, dataSize)
        dataSet1 = np.ones([10, 10])
        myBuffer.update(dataSet1)
        dataSet2 = 2 * np.ones([10, 10])
        myBuffer.update(dataSet2)
        dataSet3 = 3 * np.ones([10, 10])
        actual = myBuffer.update(dataSet3)
        result = all(x == 2 for x in actual)
        self.assertTrue(result, "Not all the first 100 elements are ones")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
