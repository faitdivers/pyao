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
        actual = myBuffer.update(dataSet)
        self.assertEquals(actual.shape, dataSize)
        result1 = np.array_equal(np.zeros([10, 10]), actual)
        self.assertTrue(result1, "Returned data is different than expected.")

    def test_udate_return_2steps(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(2, dataSize)
        dataSet1 = np.ones([10, 10])
        myBuffer.update(dataSet1)
        dataSet2 = 2 * np.ones([10, 10])
        actual = myBuffer.update(dataSet2)
        self.assertEquals(actual.shape, dataSize)
        result = np.array_equal(dataSet1, actual)
        self.assertTrue(result, "Returned data is different than expected.")

    def test_udate_return_3steps(self):
        dataSize = (10, 10)
        myBuffer = LatencyBuffer.LatencyBuffer(2, dataSize)
        dataSet1 = np.ones([10, 10])
        myBuffer.update(dataSet1)
        dataSet2 = 2 * np.ones([10, 10])
        myBuffer.update(dataSet2)
        dataSet3 = 3 * np.ones([10, 10])
        actual = myBuffer.update(dataSet3)
        result = np.array_equal(dataSet2, actual)
        self.assertTrue(result, "Returned data is different than expected.")

    def test_update_reshape(self):
        dataSize = (2, 2)
        myBuffer = LatencyBuffer.LatencyBuffer(2, dataSize)
        dataSet1 = np.array([[1, 2], [3, 4]])
        dataSet2 = np.array([[5, 6], [7, 8]])
        myBuffer.update(dataSet1)
        actual_data = myBuffer.update(dataSet2)
        result = np.array_equal(dataSet1, actual_data)
        self.assertTrue(result, "Returned data is different than expected.")

if __name__ == "__main__":
    unittest.main()
