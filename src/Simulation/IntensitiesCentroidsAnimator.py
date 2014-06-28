'''
Created on Jun 27, 2014

@author: forcaeluz
'''
import matplotlib.pyplot as plt
import SimulationAnimator as SA


class IntensitiesCentroidsAnimator(SA.SimulationAnimator):
    '''
    classdocs
    '''

    def __init__(self, name, simulation_parameters):
        '''
        Constructor
        '''
        SA.SimulationAnimator.__init__(self, name, simulation_parameters)

    def set_xy_grid(self, x, y):
        self.xlim = (x[0], x[-1])
        self.ylim = (y[0], y[-1])
        self.x = x
        self.y = y

    def set_centroids_data(self, data):
        self.centroids = data

    def set_intensities_data(self, data):
        self.intensities = data

    def _init_animation(self):
        self.ax = plt.axes(xlim=self.xlim, ylim=self.ylim)
        self.title = self.ax.set_title(self.name)
        self.intensities_plot = self.ax.pcolormesh(self.x, self.y,
                                                   self.intensities[0])
        self.centroids_plot, = self.ax.plot(self.centroids[0]['x'],
                                           self.centroids[0]['y'], '*w')

        return self.centroids_plot, self.intensities_plot

    def _update_animation(self, i):
        self.intensities_plot.set_array(self.intensities[i].ravel())
        self.centroids_plot.set_xdata(self.centroids[i]['x'])
        self.centroids_plot.set_ydata(self.centroids[i]['y'])

        return self.intensities_plot, self.centroids_plot
