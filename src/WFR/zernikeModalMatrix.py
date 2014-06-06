from numpy import *

def zernikeModalMatrix(N, l):
	
	# domain defenition
	gridx = linspace(-1,1,N)
	x,y = meshgrid(gridx, gridx)
	r = sqrt(x**2+y**2)
	
	A = zeros((N,N)) #initialize A
	idx = r<1
	A[idx] = l #every entry in idx which <1 gets the value l
	
	##Building the modal matrix
	# X derivative
	
	# Y derivative

	
	return 0
