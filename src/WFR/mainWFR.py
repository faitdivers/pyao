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
	
	#Create phase_num vector
	teller = 0
	phase_num = zeros(((x_dim+1)*(y_dim+1),1))
	for i in range(0,x_dim+1):
		for j in range(0,y_dim+1):
			#Check if the phase_id is non zero
			if phase_id[i*(x_dim+1)+j] != 0:
				phase_num[i*(x_dim+1)+j] = teller
				teller += 1
	
	#Create G matrix
	#For clarity an actual matrix shape is used
	G = zeros((2*number_slopes, teller))
	counter = 0
	for i in range(0,x_dim):
		for j in range(0,y_dim):
			if s[i*x_dim+j,0] != 0 or s[i*x_dim+j+number_slopes,0] != 0:
				#For s_x
				G[counter, phase_num[i*x_dim+j]] = -1
				G[counter, phase_num[i*x_dim+j+1]] = -1
				G[counter, phase_num[(i+1)*x_dim+j]] = 1
				G[counter, phase_num[(i+1)*x_dim+j+1]] = 1
				#For s_y
				G[counter+number_slopes, phase_num[i*x_dim+j]] = -1
				G[counter+number_slopes, phase_num[(i+1)*x_dim+j]] = -1
				G[counter+number_slopes, phase_num[i*x_dim+j+1]] = 1
				G[counter+number_slopes, phase_num[(i+1)*x_dim+j+1]] = 1
				counter += 1
	
	# syntax: ones(shape, dtype=None, order='C')
	return ones((params['numPupilx'],params['numPupily']))

