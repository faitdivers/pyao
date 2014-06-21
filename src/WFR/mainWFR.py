from numpy import *
from determinePhiPositions import determine_phi_positions
from createGeometryMatrix import create_geometry_matrix

def wfr(centroids, params, geometry):
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
	
	#Create geometry matrix
	G = create_geometry_matrix(centroids,x_dim,y_dim, geometry, D, dl)
	#Solve the least-squares problem
	# phi = (G^T G)^-1 G^T centroids
	F = dot(G.T,G) #G.T*G
	F_inv = pseudo_inverse(F)
	H = dot(F_inv,G.T)
	phi = dot(H,centroids)
	
	#Determine the physical points of the phi's 
	phiCentersX, phiCentersY = determine_phi_positions(lensCentx, lx, x_dim, lensCenty, ly, y_dim, dl, D, geometry)
	
	return phi, phiCentersX, phiCentersY

def pseudo_inverse(A):
	A_inverse = linalg.pinv(A)
	return A_inverse
