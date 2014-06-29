from numpy import *
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
	
	#Get the size of the lenslet
	D = params['D']
	#Get the distance between two lenslets
	dl = params['dl']
	
	#Create geometry matrix
	G = create_geometry_matrix(centroids,x_dim,y_dim, geometry, D, dl)
	#Solve the least-squares problem
	# phi = (G^T G)^-1 G^T centroids
	F = pseudo_inverse(G)
	phi = dot(F,centroids)
	
	return phi


def pseudo_inverse(A):
	A_inverse = linalg.pinv(A)
	return A_inverse

	
# def determine_phi_positions(lensCentx, lx, dim_x, lensCenty, ly, dim_y, dl, D):
# 	#denormalize lens center arrays
# 	lensCentersX = lensCentx*lx
# 	lensCentersY = lensCenty*ly
	
# 	#shift positions of centers to positions of phi
# 	#this is done by substracting 0.5 dl
# 	lensCentersXShifted = lensCentersX-0.5*(dl+D)
# 	lensCentersYShifted = lensCentersY-0.5*(dl+D)
	
# 	#phi consists of one more row and column
# 	#create these extra rows and columns
	
# 	#For the x positions, reshape
# 	lensCentersXShifted = lensCentersXShifted.reshape((dim_y, dim_x))
# 	#get last column
# 	last_column_x = lensCentersXShifted[:,-1]
# 	#add dl + D to get correct center
# 	last_column_phi_x = last_column_x + dl + D
# 	#otherwise we can't append it
# 	last_column_phi_x = last_column_phi_x.reshape((dim_y,1))
# 	#add this column to the phi positions of x
# 	phiCentersXAllColumns = append(lensCentersXShifted, last_column_phi_x,1)
# 	#copy the last row and append
# 	phiCentersX_last_row = phiCentersXAllColumns[-1:]
# 	phiCentersX = vstack([phiCentersXAllColumns, phiCentersX_last_row])
	
# 	#For the y positions
# 	#get the last row
# 	last_row_y = lensCentersYShifted[-dim_x:]
# 	#add dl + D to get correct centers for the new last row
# 	last_row_phi_y = last_row_y + dl + D
# 	#add the last row to the matrix
# 	phiCentersYAllRows = hstack([lensCentersYShifted,last_row_phi_y])
# 	#reshape to get last column
# 	phiCentersYAllRows = phiCentersYAllRows.reshape((dim_y+1, dim_x))
# 	#copy last column
# 	phiCentersY_last_column = phiCentersYAllRows[:,-1].reshape((dim_x+1,1))
# 	#complete centers for phi Y
# 	phiCentersY = append(phiCentersYAllRows,phiCentersY_last_column,1)
	
# 	#put them in same format as phi
# 	phiCentersX = hstack(phiCentersX)
# 	phiCentersY = hstack(phiCentersY)
	
# 	return phiCentersX, phiCentersY
	

