from numpy import *

def wfr(centroids, params):
	#Vectorize the centroids in vector s
	#s = centroids.reshape((params['numPupilx']*params['numPupily'],1))
	# syntax: ones(shape, dtype=None, order='C')
	return ones((params['numPupilx'],params['numPupily']))

