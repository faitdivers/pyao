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
        Ki = 1.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        self.assertEquals(Kp, controller.Kp);
        self.assertEquals(Ki, controller.Ki);
        self.assertEquals(Kd, controller.Kd);

    def testSisoControllerFirstStep(self):
        """ Tests if the controller reacts as expected in a SISO model
        
        """
        Kp = 1.0
        Ki = 1.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        output = controller.update(10);
        self.assertEquals(31, output)
        
    def testMiMoControllerFirstStep(self):
        """ Tests if the controller can handle arrays as input and output.
        
        """
        Kp = 1.0
        Ki = 1.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        inputArray = array([1, 2, 3, 4]);
        expectedOutput = array([3.1, 6.2, 9.3, 12.4])
        output = controller.update(inputArray);
        testSucceded = allclose(expectedOutput, output)
        self.assert_(testSucceded, "Array comparison not close enough")
        
    def testSisoControllerSecondStep(self):
        """ Tests if the controller handles integration and derivation correctly
        over multiple steps.
        """
        Kp = 1.0
        Ki = 1.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        controller.update(1)
        output = controller.update(2)
        self.assertEquals(6.1, output)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstructor']
    unittest.main()
