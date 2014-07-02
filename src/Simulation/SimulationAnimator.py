'''
Created on Jun 27, 2014

@author: forcaeluz
'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class SimulationAnimator():
    ''' Generic simulation class

    '''

    def __init__(self, name, simulation_parameters):
        self.name = name
        self.time = simulation_parameters['time']
        self.frequency = simulation_parameters['frequency']
        self.iterations = self.time * self.frequency
        return

    def _init_animation(self):
        return

    def _update_animation(self, i):
        return

    def plot_animation(self):
        self.fig = plt.figure()
        self.ani = animation.FuncAnimation(self.fig, self._update_animation,
                                           frames=self.iterations,
                                           interval=(1000 / self.frequency),
                                           blit=True,
                                           init_func=self._init_animation)

        self.ani.save("%s.mp4" % self.name, fps=self.frequency,
                      codec='libx264')
        return
