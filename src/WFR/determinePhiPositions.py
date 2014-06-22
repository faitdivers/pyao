from numpy import *
import sys

def determine_phi_positions(lensCentx, lx, dim_x, lensCenty, ly, dim_y, dl, D, geometry):
	if geometry == 'fried':
		phiCentersX, phiCentersY = phi_positions_fried(lensCentx, lx, dim_x, lensCenty, ly, dim_y, dl, D)
	elif geometry == 'southwell':
		phiCentersX, phiCentersY = phi_positions_southwell(lensCentx, lx, lensCenty, ly)
	elif geometry == 'mhudgin':
		print 'modified Hudgin'
	else:
		print 'Unknown Geometry chosen'
		sys.exit()
	return phiCentersX, phiCentersY
	
def phi_positions_fried(lensCentx, lx, dim_x, lensCenty, ly, dim_y, dl, D):
	#denormalize lens center arrays
	lensCentersX = lensCentx*lx
	lensCentersY = lensCenty*ly
	
	#shift positions of centers to positions of phi
	#this is done by substracting 0.5 dl
	lensCentersXShifted = lensCentersX-0.5*(dl+D)
	lensCentersYShifted = lensCentersY-0.5*(dl+D)
	
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
	phiCentersY_last_column = phiCentersYAllRows[:,-1].reshape((dim_y+1,1))
	#complete centers for phi Y
	phiCentersY = append(phiCentersYAllRows,phiCentersY_last_column,1)
	
	#put them in same format as phi
	phiCentersX = hstack(phiCentersX)
	phiCentersY = hstack(phiCentersY)
	
	return phiCentersX, phiCentersY
		
def phi_positions_southwell(lensCentx, lx, lensCenty, ly):
	#phi positions at the same spot as the slopes/lenses
	#denormalize lens center arrays
	phiCentersX = lensCentx*lx
	phiCentersY = lensCenty*ly
	
	return phiCentersX, phiCentersY
