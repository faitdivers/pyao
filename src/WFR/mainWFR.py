from numpy import *

def wfr(centroids, params):
	#Get dimensions
	x_dim = params['noApertx']
	y_dim = params['noAperty']
	number_slopes = x_dim*y_dim
	
	s = centroids
	
	#Create a phase_id vector
	phase_id = zeros(((x_dim+1)*(y_dim+1),1))
	for i in range(0,x_dim):
		for j in range(0,y_dim):
			#Check if the slope at s(i,j) is non zero
			#Put a 1 at each place of phi we need
			if s[i*x_dim+j,0] != 0 or s[i*x_dim+j+number_slopes,0] != 0:
				phase_id[i*x_dim+j,0] = 1
				phase_id[i*x_dim+j+1,0] = 1
				phase_id[(i+1)*x_dim+j,0] = 1
				phase_id[(i+1)*x_dim+j+1,0] = 1
				
	
	# syntax: ones(shape, dtype=None, order='C')
	return ones((params['numPupilx'],params['numPupily']))

