'''
Created on Jun 25, 2014

@author: forcaeluz
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.pyplot import ylim

class WavefronAnimator:
    ''' WavefrontAnimator class
    
    This class provides animation capabilities, to generate
    short movies of the simulations.
    '''


    def __init__(self, simulation_parameters, sensor_parameters):
        '''
        
        '''
        self.Nx = sensor_parameters['numPupilx'] # Samples on the x-axis
        self.Ny = sensor_parameters['numPupily'] # Samples on the y_axis
        self.lx = sensor_parameters['lx'] # Width of the sensor plane in the x-direction [m]
        self.ly = sensor_parameters['ly'] # Width of the sensor plane in the y-direction [m]
        
        self.time = simulation_parameters['time']
        self.frequency = simulation_parameters['frequency']
        self.iterations = self.time * self.frequency
        
    
    def set_wavefront_data(self, data):
        if len(data) == self.iterations:
            self.data = data
        else:
            print("WARNING: Supplied simulation data does not contain the"
                    + " correct amount of samples")
    
    
    def set_plot_title(self, title):
        self.title = title
        
    
    def compute_xy_grid(self):
        # Create grid for in the focal plane
        dx = self.lx/self.Nx # Sample length on x-axis [m]
        dy = self.ly/self.Ny # Sample length on y-axis [m]
        self.x = np.arange(0.0, self.lx + dx, dx) # Sample positions on x-axis [m]
        self.y = np.arange(0.0, self.ly + dy, dy) # Sample positions on y-axis [m]

               
    def _init_animation(self):
        self.compute_xy_grid()
        self.ax = plt.axes(xlim=(0, self.lx), ylim=(0, self.ly))
        self.title = self.ax.set_title("Wavefront plot")
        self.wavefrontPlot = self.ax.pcolormesh(self.x, self.y, self.data[0])
        return self.wavefrontPlot, self.title
        
    def _animate(self, i):
        wf_to_plot = self.data[i]
        wf_to_plot = wf_to_plot[:, :]
        time_stamp = i * (1 / self.frequency)
        self.wavefrontPlot.set_array(wf_to_plot.ravel())
        self.title.set_text("Wavefront at time: %f" % (time_stamp))
        return self.wavefrontPlot, self.title
        
    
    def plot_animation(self):
        self.fig = plt.figure()
        self.ani = animation.FuncAnimation(self.fig, self._animate, frames=self.iterations,
                                          interval=(1000 / self.frequency), blit=True, 
                                          init_func=self._init_animation)
        self.ani.save("wavefront.mp4", fps=10, codec='libx264')

