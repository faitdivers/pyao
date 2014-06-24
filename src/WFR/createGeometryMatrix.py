from numpy import *

def create_geometry_matrix(centroids,x_dim,y_dim, geometry, D, dl):
	if geometry == 'fried':
		phase_id = create_phase_id(centroids, x_dim, y_dim)
		phase_num, counter = create_phase_num(phase_id, x_dim, y_dim, geometry)
		G = create_Friedmap(centroids, phase_num, counter, x_dim, y_dim, dl)
	elif geometry == 'southwell':
		phase_id = None
		phase_num = create_phase_num(phase_id, x_dim, y_dim, geometry)
		G = create_Southwellmap(x_dim, y_dim, phase_num,dl)
	elif geometry == 'mhudgin':
		print 'modified Hudgin'
	else:
		print '[WFR] Unknown geometry chosen'
		sys.exit()
	return G

def create_phase_id(centroids, x_dim, y_dim):
	#Create a phase_id matrix
	number_slopes = x_dim*y_dim
	phase_id = zeros(((x_dim+1),(y_dim+1)),dtype=int)
	for i in range(0,x_dim):
		for j in range(0,y_dim):
			#Check if the slope at s(i,j) is non zero
			#Put a 1 at each place of phi we need
			#if centroids[i*x_dim+j,0] != 0 or centroids[i*x_dim+j+number_slopes,0] != 0:
			phase_id[i,j] = 1
			phase_id[i,j+1] = 1
			phase_id[i+1,j] = 1
			phase_id[i+1,j+1] = 1
	return phase_id
	
def create_phase_num(phase_id,x_dim,y_dim,geometry):
	if geometry == 'fried' or geometry == 'mhudgin':
		#Create phase_num matrix
		counter = 0
		phase_num = zeros(((x_dim+1),(y_dim+1)),dtype=int)
		for i in range(0,x_dim+1):
			for j in range(0,y_dim+1):
				#Check if the phase_id is non zero
				if phase_id[i,j] != 0:
					phase_num[i,j] = counter
					counter += 1
		return phase_num, counter
	elif geometry == 'southwell':
		number_slopes = x_dim*y_dim
		#create phase_num matrix
		phase_num = arange(number_slopes).reshape((y_dim, x_dim))
		return phase_num
	
def create_Friedmap(centroids, phase_num, counter, x_dim, y_dim, Dl):
	#Create G matrix
	#For clarity an actual matrix shape is used
	number_slopes = x_dim*y_dim
	G = zeros((2*number_slopes, counter),dtype=int)
	counter = 0
	for i in range(0,x_dim):
		for j in range(0,y_dim):
			if centroids[i*x_dim+j,0] != 0 or centroids[i*x_dim+j+number_slopes,0] != 0:
				#For s_x
				G[counter, phase_num[i,j]] = -1/(2*Dl)
				G[counter, phase_num[i,j+1]] = -1/(2*Dl)
				G[counter, phase_num[i+1,j]] = 1/(2*Dl)
				G[counter, phase_num[i+1,j+1]] = 1/(2*Dl)
				#For s_y
				G[counter+number_slopes, phase_num[i,j]] = -1/(2*Dl)
				G[counter+number_slopes, phase_num[i+1,j]] = -1/(2*Dl)
				G[counter+number_slopes, phase_num[i,j+1]] = 1/(2*Dl)
				G[counter+number_slopes, phase_num[i+1,j+1]] = 1/(2*Dl)
				counter += 1
	return G
def create_mHudginmap(centroids, phase_num, counter, x_dim, y_dim, D):
	print 'hudgin map'

def create_Southwellmap(x_dim,y_dim,phase_num, dl):
	number_slopes = x_dim*y_dim
	#create empty matrices
	Cx = zeros(((x_dim-1)*y_dim,number_slopes))
	Cy = zeros((x_dim*(y_dim-1),number_slopes))
	
	#Fill Cx which is linking \Sigma_x to sigma_x
	counter = 0
	for i in range(0,y_dim):
		for j in range(0,x_dim-1):
			Cx[counter, phase_num[i,j]] = -1
			Cx[counter, phase_num[i,j+1]] = 1
			counter += 1
	
	#Fill Cy which is linking \Sigma_y to sigma_y
	counter = 0
	for i in range(0,y_dim-1):
		for j in range(0,x_dim):
			Cy[counter, phase_num[i,j]] = -1
			Cy[counter, phase_num[i+1,j]] = 1
			counter += 1
	
	#Zeros for filling up the A matrix
	zero_x = zeros(((x_dim-1)*y_dim,number_slopes))
	zero_y = zeros((x_dim*(y_dim-1),number_slopes))
	
	#Construct the A matrix
	#A = [Cx zero_x; zero_y, Cy]/2
	A = vstack([hstack([Cx,zero_x]),hstack([zero_y,Cy])])/2
	
	#Construct the B matrix
	#B = [Cx; Cy]/dl
	B = vstack([Cx,Cy])/dl
	
	#Construct G matrix
	# G = A^-1*B 
	Ainv = linalg.pinv(A)
	G = dot(Ainv,B)
	
	return G 
	
	
	
	
