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
	
	#Get lenslet centers
	lensCentx = params['lensCentx']
	lensCenty = params['lensCenty']
	lx = params['lx']
	ly = params['ly']
	
	#Get the size of the lenslet
	D = params['D']
	#Get the distance between two lenslets
	dl = params['dl']
	
	#Create phase_id matrix
	phase_id = create_phase_id(centroids,x_dim,y_dim)
	#Create phase_num matrix
	phase_num, teller = create_phase_num(phase_id,x_dim,y_dim)
	#Create Fried matrix
	G = create_Friedmap(centroids, phase_num, teller, x_dim, y_dim, D)
	#Solve the least-squares problem
	# phi = (G^T G)^-1 G^T centroids
	F = dot(G.T,G) #G.T*G
	F_inv = pseudo_inverse(F)
	H = dot(F_inv,G.T)
	phi = dot(H,centroids)
	
	#Determine the physical points of the phi's 
	phiCentersX, phiCentersY = determine_phi_positions(lensCentx, lx, x_dim, lensCenty, ly, y_dim, dl, D)
	
	return phi, phiCentersX, phiCentersY

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

def create_Friedmap(centroids, phase_num, teller, x_dim, y_dim, Dl):
	#Create G matrix
	#For clarity an actual matrix shape is used
	number_slopes = x_dim*y_dim
	G = zeros((2*number_slopes, teller),dtype=int)
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

def pseudo_inverse(A):
	A_inverse = linalg.pinv(A)
	return A_inverse
	
def determine_phi_positions(lensCentx, lx, dim_x, lensCenty, ly, dim_y, dl, D):
	#denormalize lens center arrays
	lensCentersX = lensCentx*lx
	lensCentersY = lensCenty*ly
	
	#shift positions of centers to positions of phi
	#this is done by substracting 0.5 dl
	lensCentersXShifted = lensCentersX-0.5*dl
	lensCentersYShifted = lensCentersY-0.5*dl
	
	#phi consists of one more row and column
	#create these extra rows and columns
	
	#For the x positions, reshape
	lensCentersXShifted = lensCentersXShifted.reshape((dim_y, dim_x))
	#get last column
	last_column_x = lensCentersXShifted[:,-1]
	#add dl + D to get correct center
	last_column_phi_x = last_column_x + dl + D
	#otherwise we can't append it
	last_column_phi_x = last_column_phi_x.reshape((dim_y,1))
	#add this column to the phi positions of x
	phiCentersXAllColumns = append(lensCentersXShifted, last_column_phi_x,1)
	#copy the last row and append
	phiCentersX_last_row = phiCentersXAllColumns[-1:]
	phiCentersX = vstack([phiCentersXAllColumns, phiCentersX_last_row])
	
	#For the y positions
	#get the last row
	last_row_y = lensCentersYShifted[-dim_x:]
	#add dl + D to get correct centers for the new last row
	last_row_phi_y = last_row_y + dl + D
	#add the last row to the matrix
	phiCentersYAllRows = hstack([lensCentersYShifted,last_row_phi_y])
	#reshape to get last column
	phiCentersYAllRows = phiCentersYAllRows.reshape((dim_y+1, dim_x))
	#copy last column
	phiCentersY_last_column = phiCentersYAllRows[:,-1].reshape((dim_x,1))
	#complete centers for phi Y
	phiCentersY = append(phiCentersYAllRows,phiCentersY_last_column,1)
	
	#put them in same format as phi
	phiCentersX = hstack(phiCentersX)
	phiCentersY = hstack(phiCentersY)
	
	return phiCentersX, phiCentersY
	
