'''
Created on May 17, 2014

@author: forcaeluz
'''
from numpy import array, ndarray

class PIDcontroller:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.currentInput = 0
        self.oldInput = 0
        self.integration = 0
        self.integrationMax = 500
        self.integrationMin = -500
        
    def update(self, current):
        self.oldInput = self.currentInput
        self.currentInput = current
        
        P = self._calculateP()
        I = self._calculateI()
        D = self._calculateD()
        
        return P + I + D;
    
    def setKp(self, Kp):
        self.Kp = Kp
    
    def getKp(self):
        return self.Kp
        
    def setKi(self, Ki):
        self.Ki = Ki
        
    def setKd(self, Kd):
        self.Kd = Kd
        
    def _calculateP(self):
        """ Calculate the proportional effect on the controller output.
        """
        return self.Kp * self.currentInput
        
    def _calculateI(self):
        """ Calculate the integrator effect on the controller output.
        
        On the integrator anti-wind up is applied.
        """
        self.integration += self.currentInput
        if isinstance(self.integration, ndarray):
            self.integration = array([self._calculate_antiwindup(x) for x in self.integration])
        else:
            self.integration = self._calculate_antiwindup(self.integration)
                
        return self.Ki * self.integration
        
    def _calculateD(self):
        """ Calculate the derivative effect on the controller output.
        """
        deltaInput = self.currentInput - self.oldInput
        return self.Kd * deltaInput
        
    def _calculate_antiwindup(self, integration):
            if integration > self.integrationMax:
                limitedIntegration = self.integrationMax
            elif integration < self.integrationMin:
                limitedIntegration = self.integrationMin
            else:
                limitedIntegration = integration
                
            return limitedIntegration
