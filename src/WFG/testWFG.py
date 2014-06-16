import numpy
numpy.set_printoptions(threshold=numpy.nan)
from numpy import allclose, load
from zernike import *

import unittest
import os

#unittest.TestCase
class TestZernikeWavefront(unittest.TestCase):
    def testConstructor(self):
        zernikeModes = [2,4,21]
        zernikeWeights = [0.5,0.25,-0.6]        
       
        zw = ZernikeWave()
        zw.addMode(zernikeModes, zernikeWeights)
        
	self.assertTrue(zernikeModes,zw.getModes())
	self.assertTrue(zernikeWeights, zw.getWeights())

    def loadTestData(self, fileName):
        script_dir = os.path.dirname(__file__)
        rel_path = fileName
        abs_file_path = os.path.join(script_dir, rel_path)
        data = load(abs_file_path)
        return data
    
    def testWavefront(self):        
        data = self.loadTestData('defocusTestData.npy')
        paramt = {
        'numPupilx' : 11,
        'numPupily' : 11,
        'numImagx' : 50,
        'numImagy' : 50,
        'noApertx': 5,
        'noAperty': 5
        }
        zernikeModes = [2,4,21]
        zernikeWeights = [0.5,0.25,-0.6]
        
        zw = ZernikeWave()
        zw.addMode(zernikeModes, zernikeWeights)
        wf = zw.createWavefront(paramt['numImagx'],paramt['numImagy'])
        
        self.assertEqual(data,wf)

    def testWavefrontDecomposition(self):
        paramt = {
        'numPupilx' : 11,
        'numPupily' : 11,
        'numImagx' : 50,
        'numImagy' : 50,
        'noApertx': 5,
        'noAperty': 5
        }
        zernikeModes = [2,4,21]
        zernikeWeights = [0.5,0.25,-0.6]
        
        zw = ZernikeWave()
        zw.addMode(zernikeModes, zernikeWeights)
        wf = zw.createWavefront(paramt['numImagx'],paramt['numImagy'])
        Z,A = zw.decomposeWavefront(wf)
        
        testResult = allclose(reshape(A,(1,len(A))), zw.getWeights())
        self.assertTrue(testResult)
        
    def testNollMapping(self):
        data = self.loadTestData('indexTestData.npy')
        datastr = ""
        for n in range(1,81):
            u,v = zernikeIndex(n)
            datastr = datastr + "%d: (%d,%d) " %(n,u,v)
        
        self.assertEqual(data,datastr)

if __name__ == "__main__":
    unittest.main()
