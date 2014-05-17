'''
Created on May 17, 2014

@author: forcaeluz
'''
import unittest
import PIDController

from numpy import array
from numpy import allclose

class Test(unittest.TestCase):


    def testConstructor(self):
        """ Tests if the constructor assign the right variables
        """
        Kp = 1.0
        Ki = 0.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        self.assertEquals(Kp, controller.Kp);
        self.assertEquals(Ki, controller.Ki);
        self.assertEquals(Kd, controller.Kd);

    def testSisoControllerFirstStep(self):
        """ Tests if the controller reacts as expected in a SISO model
        
        """
        Kp = 1.0
        Ki = 0.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        output = controller.update(10);
        self.assertEquals(21, output)
        
    def testMiMoControllerFirstStep(self):
        """ Tests if the controller can handle arrays as input and output.
        
        """
        Kp = 1.0
        Ki = 0.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        inputArray = array([1, 2, 3, 4]);
        expectedOutput = array([2.1, 4.2, 6.3, 8.4])
        output = controller.update(inputArray);
        testSucceded = allclose(expectedOutput, output)
        self.assert_(testSucceded, "Array comparison not close enough")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstructor']
    unittest.main()