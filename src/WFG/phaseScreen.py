#from scipy import *
import numpy as np
#from math import *
import supportWFG as supp

import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3

class PhaseScreen:
    def __init__(self):
        self.screenType = ""
        self.params = []

    def setType(self, phaseScreenType = 'Kolmogorov'):
        if phaseScreenType == 'Kolmogorov':
            self.screenType = 'Kolmogorov'
            self.params = [0]
        elif phaseScreenType == 'vonKarman':
            self.screenType = 'vonKarman'
            self.params = [0,0,0]
        #
        # Add other screen types here
        #
        else:
            print('ERROR: A valid phase screen type must be specified')
            return
    
    def getType(self):
        return self.screenType                        
                
    def setParams(self,parameters):
        if self.screenType != "":
            if self.screenType == 'Kolmogorov':
                 if 'r0' in parameters:
                     self.params[0] = parameters['r0']
                 else:
                     print('ERROR: Not all required terms are specified for Kolmogorov.')
                     return
            elif self.screenType == 'vonKarman':
                 if ('r0' in parameters) and ('l0' in parameters) and ('L0' in parameters):
                     self.params[0] = parameters['r0']
                     self.params[1] = parameters['l0']
                     self.params[2] = parameters['L0']
                 else:
                     print('ERROR: Not all required terms are specified for von Karman.')
                     return
            #               
            # Add other screen types here
            #
            else:
                print('ERROR: Some internal error occured.')
                return
        else:
            print('ERROR: Specify a phase screen type first.')
    
    def getParameters(self):
        if self.screenType == "":
            print('ERROR: No type of distortion selected yet.')
            return None
        elif self.screenType == 'Kolmogorov':
            return {'r0' : self.params[0]}
        elif self.screenType == 'vonKarman':
            return {'r0' : self.params[0], 'l0' : self.params[1], 'L0' : self.params[2]}
        else:
            print('Error: Some internal error occured')
            return None
    
    def createWavefront(self,nX,nY):
        if nX != nY:
            print('WARNING: Unequal spatial/frequency spacing in x and y-direction., using nX from now on.')
        
        if self.screenType == 'Kolmogorov':
            r0 = self.params[0]
            WF = self.kolmogorov(nX,r0)
        elif self.screenType == 'vonKarman':
            r0 = self.params[0]
            l0 = self.params[1]
            L0 = self.params[2]
            WF = self.vonKarman(nX,r0,l0,L0)
        else: 
            print('ERROR: Some internal error occured.')
            WF = None
            return
            
        return WF
                    
    def kolmogorov(self,N, r0, D = 2.):
        delta = D / N        
        phi_l = np.zeros((N,N))
        
        X,Y = supp.createGrid(N, N, [delta*(N/2), delta*((N/2) - 1)], [delta*(N/2), delta*((N/2) - 1)])
 
        for pp in range(1,4):
            delta_f = 1./(3**(pp*D))
            
            fx = delta_f*np.array([-1.,0.0,1.])
            Fx, Fy = np.meshgrid(fx,fx)
            Rf, Tf = supp.cart2pol(Fx,Fy)
            
            print Rf
            print r0
            
            # Kolmogorov
            PSD_phi = 0.023*r0**(-5/3) * Rf**(-11/3)
            PSD_phi[1,1] = 0
                                    
            cn = (np.array(np.random.randn(3,3)) + np.array(np.random.randn(3,3))*1j) * np.sqrt(PSD_phi) * delta_f
            SH = np.zeros((N,N))
            
            cn = np.reshape(cn,9,'F')
            Fx = np.reshape(Fx,9,'F')
            Fy = np.reshape(Fy,9,'F')
            for s in range(0,9):
                 SH = SH + cn[s] * np.exp(1j * 2 * np.pi * (Fx[s]*X * Fy[s]*Y))
             
            phi_l  = phi_l + SH       
        phi_l = np.real(phi_l) - np.mean(np.real(phi_l))
        
        return phi_l
        
    def vonKarman(self,N, r0, l0, L0, D = 2):
        delta = D / N        
        phi_l = np.zeros((N,N))
        
        X,Y = supp.createGrid(N, N, [delta*(N/2), delta*((N/2) - 1)], [delta*(N/2), delta*((N/2) - 1)])
        
        fm = 5.92/(2*np.pi*l0)
        f0 = 1/L0
             
        for pp in range(1,4):
            delta_f = 1./(3**(pp*D))
            
            fx = delta_f*np.array([-1.,0.0,1.])
            Fx, Fy = np.meshgrid(fx,fx)
            Rf, Tf = supp.cart2pol(Fx,Fy)
                    
            #von Karman
            PSD_phi = (0.023*r0**(-5/3)* np.exp(-(Rf/fm)**2)) / ((Rf**2 + f0**2)**(11/6))
            PSD_phi[1,1] = 0
                                    
            cn = (np.array(np.random.randn(3,3)) + np.array(np.random.randn(3,3))*1j) * np.sqrt(PSD_phi) * delta_f
            SH = np.zeros((N,N))
            
            cn = np.reshape(cn,9,'F')
            Fx = np.reshape(Fx,9,'F')
            Fy = np.reshape(Fy,9,'F')
            for s in range(0,9):
                 SH = SH + cn[s] * np.exp(1j * 2 * np.pi * (Fx[s]*X * Fy[s]*Y))
             
            phi_l  = phi_l + SH
                
        phi_l = np.real(phi_l) - np.mean(np.real(phi_l))
        
        return phi_l
        
    def plotWavefront(self,nX,nY):
        X,Y = supp.createGrid(nX,nY)
        WF = self.createWavefront(nX,nY)
        #print WF
        title = "Combined Phase, \phi(x), of the  Wavefront"
        # Plot results in a surface plot
        fig = p.figure();
        ax = p3.Axes3D(fig)
        ax.plot_surface(X,Y,WF, rstride=1, cstride=1, cmap='jet')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel(title)
        p.show()    
