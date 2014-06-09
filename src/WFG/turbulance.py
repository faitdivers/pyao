from scipy import *
import numpy
from math import *
from nollMap import *
from supportWFG import *

import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3

# Structure for generating distortions:
# Create frequency grid: df = 1/(N_i*delta_i)
#                        f_i = (N/2 : N/2 - 1)*df
#                        [F_i] = meshgrid(f_i)
# Polar grid:            [F_p] = cart2pol(f_i)
# Power Spectrum density: PSD_phi(f,th)
