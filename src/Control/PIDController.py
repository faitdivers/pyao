'''
Created on May 17, 2014

@author: forcaeluz
'''

class PIDcontroller:
    
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.currentInput = 0
        self.oldInput = 0
        self.integration = 0
        
    def update(self, current):
        self.oldInput = self.currentInput
        self.currentInput = current
        
        P = self._calculateP()
        I = self._calculateI()
        D = self._calculateD()
        
        return P + I + D;
    
    def _calculateP(self):
        """ Calculate the proportional effect on the controller output.
        """
        return self.Kp * self.currentInput
        
    def _calculateI(self):
        """ Calculate the integrator effect on the controller output
        
        TODO: Should be implemented when an integration action is required in the PID
        controller.
        """
        return 0
        
    def _calculateD(self):
        """ Calculate the derivative effect on the controller output.
        """
        deltaInput = self.oldInput - self.currentInput
        return self.Kd * deltaInput
        
    def setKp(self, Kp):
        self.Kp = Kp
        
    def setKi(self, Ki):
        self.Ki = Ki
        
    def setKd(self, Kd):
        self.Kd = Kd