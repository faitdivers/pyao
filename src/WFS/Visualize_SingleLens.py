#Visualization for Single Lens System 
#Updated: May 28, 2014
#Project: PyAO
#Description: Allows for testing/visualization of the SingleLens solution. 
#             Calls wfs from mainWFS.py for the numerical solution, then calls 
#             wfs_Plot to calculate the analytical solution and plot both 
#             solutions. This file stands alone from the PyAO project main. 

from mainWFS import *
from SingleLens import *

# Copy of paramsSensor from main, since it can't be retrieved from the parent directory 	
pS = {
# number of samples in the pupil plane
'numPupilx' : 100,
'numPupily' : 100,
# number of samples in the imaging plane(s)
'numImagx' : 100,
'numImagy' : 100,
# number of apertures in the wfs
'noApertx': 10,
'noAperty': 10,
# focal distance, pixel length, sizes/diameters of the apertures, ...
'F': 18e-3,    		# Focal Length [m]
'Diam': 300e-6, 	# Diameter of pupil [m] - of system or lenslet?
'lam': 630e-9, 		# Wavelength [m]
'Lx': 4000e-6, 		# Support Width in x dimension (real space) [m]
'Ly': 4000e-6, 		# Support Width in y dimension (real space) [m]
}

wf = 1	
I_i = wfs(wf, pS)
wfs_Plot(I_i, wf, pS)