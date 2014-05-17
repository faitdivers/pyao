'''
Created on May 17, 2014

@author: forcaeluz
'''
import unittest
import PIDController

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
        Kp = 1.0
        Ki = 0.0
        Kd = 1.1
        controller = PIDController.PIDcontroller(Kp, Ki, Kd)
        output = controller.update(10);
        self.assertEquals(21, output)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstructor']
    unittest.main()