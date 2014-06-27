'''
Created on Jun 25, 2014

@author: forcaeluz
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class WavefronAnimator:
    ''' WavefrontAnimator class

    This class provides animation capabilities, to generate
    short movies of the simulations.
    '''

    def __init__(self, simulation_parameters, sensor_parameters):
        ''' Constructor

        Keyword arguments:
        simulation_parameters -- Dictionary with simulation parameters
        sensor_parameters -- Dictionary with sensor parameters
        '''
        self.Nx = sensor_parameters['numPupilx']
        self.Ny = sensor_parameters['numPupily']
        self.lx = sensor_parameters['lx']
        self.ly = sensor_parameters['ly']

        self.time = simulation_parameters['time']
        self.frequency = simulation_parameters['frequency']
        self.iterations = self.time * self.frequency

    def set_wavefront_data(self, data):
        ''' Set the data that will be plotted.
        '''
        if len(data) == self.iterations:
            self.data = data
        else:
            print("WARNING: Supplied simulation data does not contain the"
                    + " correct amount of samples")

    def set_plot_title(self, title):
        self.title = title

    def compute_xy_grid(self):
        ''' Compute the boundaries for each pixel in the x and y directions

        TODO:
            In the future we should check how to address the generation and the
            plotting of data, and document it properly. Then this function most
            likely will have to be changed.
        '''
        dx = self.lx / self.Nx
        dy = self.ly / self.Ny
        self.x = np.arange(0.0, self.lx + dx, dx)
        self.y = np.arange(0.0, self.ly + dy, dy)

    def _init_animation(self):
        ''' Initializes the animation.

        '''
        self.compute_xy_grid()
        self.ax = plt.axes(xlim=(0, self.lx), ylim=(0, self.ly))
        self.title = self.ax.set_title("Wavefront plot")
        self.wavefrontPlot = self.ax.pcolormesh(self.x, self.y, self.data[0])
        return self.wavefrontPlot, self.title

    def _animate(self, i):
        ''' Plot each step of the animation
        '''
        wf_to_plot = self.data[i]
        time_stamp = i * (1 / self.frequency)
        self.wavefrontPlot.set_array(wf_to_plot.ravel())
        self.title.set_text("Wavefront at time: %f" % (time_stamp))
        return self.wavefrontPlot, self.title

    def plot_animation(self):
        ''' The public interface to generate the animation.
        '''
        self.fig = plt.figure()
        self.ani = animation.FuncAnimation(self.fig, self._animate,
                                           frames=self.iterations,
                                           interval=(1000 / self.frequency),
                                           blit=True,
                                           init_func=self._init_animation)

        self.ani.save("wavefront.mp4", fps=10, codec='libx264')
