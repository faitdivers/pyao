from numpy import *

def wfr(centroids, params):
	""" Compute the reconstructed wavefront

	Reconstruct the wavefront from the received slopes
	Expected input: [s_x(0,0),...,s_x(0,N),...,s_x(M,0),...,s_x(M,N),s_y(0,0),...,s_y(0,N),...,s_y(M,0),...,s_y(M,N)]^T
	
	Returns:
		The phi matrix in the form [phi(0,0),...,phi(0,P),...,phi(Q,0),...,phi(P,Q)]^T
	"""
	#Get dimensions
	x_dim = params['noApertx']
	y_dim = params['noAperty']
	
	#Create phase_id matrix
	phase_id = create_phase_id(centroids,x_dim,y_dim)
	#Create phase_num matrix
	phase_num, teller = create_phase_num(phase_id,x_dim,y_dim)
	#Create G matrix
	G = create_G(centroids, phase_num, teller, x_dim, y_dim)
	print('G = \n{}'.format(G))	
	
	#Inversion
	G_inverse = pseudo_inverse(G)
	print('G_inverse = \n{}'.format(G_inverse))
	
	# syntax: ones(shape, dtype=None, order='C')
	return ones((params['numPupilx'],params['numPupily']))

def create_phase_id(centroids, x_dim, y_dim):
	#Create a phase_id matrix
	number_slopes = x_dim*y_dim
	phase_id = zeros(((x_dim+1),(y_dim+1)),dtype=int)
	for i in range(0,x_dim):
		for j in range(0,y_dim):
			#Check if the slope at s(i,j) is non zero
			#Put a 1 at each place of phi we need
			if centroids[i*x_dim+j,0] != 0 or centroids[i*x_dim+j+number_slopes,0] != 0:
				phase_id[i,j] = 1
				phase_id[i,j+1] = 1
				phase_id[i+1,j] = 1
				phase_id[i+1,j+1] = 1
	return phase_id
	
def create_phase_num(phase_id, x_dim, y_dim):
		#Create phase_num matrix
	teller = 0
	phase_num = zeros(((x_dim+1),(y_dim+1)),dtype=int)
	for i in range(0,x_dim+1):
		for j in range(0,y_dim+1):
			#Check if the phase_id is non zero
			if phase_id[i,j] != 0:
				phase_num[i,j] = teller
				teller += 1
	return phase_num, teller

def create_G(centroids, phase_num, teller, x_dim, y_dim):
	#Create G matrix
	#For clarity an actual matrix shape is used
	number_slopes = x_dim*y_dim
	G = zeros((2*number_slopes, teller),dtype=int)
	counter = 0
	for i in range(0,x_dim):
		for j in range(0,y_dim):
			if centroids[i*x_dim+j,0] != 0 or centroids[i*x_dim+j+number_slopes,0] != 0:
				#For s_x
				G[counter, phase_num[i,j]] = -1
				G[counter, phase_num[i,j+1]] = -1
				G[counter, phase_num[i+1,j]] = 1
				G[counter, phase_num[i+1,j+1]] = 1
				#For s_y
				G[counter+number_slopes, phase_num[i,j]] = -1
				G[counter+number_slopes, phase_num[i+1,j]] = -1
				G[counter+number_slopes, phase_num[i,j+1]] = 1
				G[counter+number_slopes, phase_num[i+1,j+1]] = 1
				counter += 1
	return G

def pseudo_inverse(A):
	A_inverse = linalg.pinv(A)
	return A_inverse
	
