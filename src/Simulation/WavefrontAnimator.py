'''
Created on Jun 25, 2014

@author: forcaeluz
'''

import matplotlib.pyplot as plt
import SimulationAnimator as SA


class WavefronAnimator(SA.SimulationAnimator):
    ''' WavefrontAnimator class

    This class provides animation capabilities, to generate
    short movies of the simulations.
    '''

    def __init__(self, name, simulation_parameters):
        ''' Constructor

        Keyword arguments:
        name -- Name for the movie file and plot title
        simulation_parameters -- Dictionary with simulation parameters
        '''
        SA.SimulationAnimator.__init__(self, name, simulation_parameters)

    def set_wavefront_data(self, data):
        self.data = data

    def set_plot_title(self, title):
        self.title = title

    def set_xy_grid(self, x, y):
        self.xlim = (x[0], x[-1])
        self.ylim = (y[0], y[-1])
        self.x = x
        self.y = y

    def _init_animation(self):
        ''' Initializes the animation.

        '''
        self.ax = plt.axes(xlim=self.xlim, ylim=self.ylim)
        self.title = self.ax.set_title(self.name)
        self.wavefrontPlot = self.ax.pcolormesh(self.x, self.y, self.data[0])
        return self.wavefrontPlot

    def _update_animation(self, i):
        ''' Plot each step of the animation
        '''
        wf_to_plot = self.data[i]
        self.wavefrontPlot.set_array(wf_to_plot.ravel())
        return self.wavefrontPlot
