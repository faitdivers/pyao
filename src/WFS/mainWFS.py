#Lenslet Array
#Updated: Juni 10, 2014
import math
from numpy import *
from scipy import *
import numpy.fft
from scipy import interpolate

def wfs(phaseIn, paramsSensor):
	# Unwrap paramsSensor
	Nx = paramsSensor['numPupilx'] # Samples on the x-axis
	Ny = paramsSensor['numPupily'] # Samples on the y_axis
	lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
	ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
	lensCentx = paramsSensor['lensCentx'] # Lenslet centers on x-axis [m]
	lensCenty = paramsSensor['lensCenty'] # Lenslet centers on y-axis [m]
	f = paramsSensor['f'] # Focal length [m]
	D = paramsSensor['D'] # Lens diameter [m]
	lam = paramsSensor['lam'] # Wavelength [m]
	supFactor = paramsSensor['supportFactor'] # Support factor
	supD = D*supFactor # Support diameter for each lenslet [m]
	k = 2*pi/lam # Wavenumber
	
	# Create grid for in the focal plane
	dx = lx/(Nx - 1.0) # Sample length on x-axis [m]
	dy = ly/(Ny - 1.0) # Sample length on y-axis [m]
	x = arange(0.0, lx + dx, dx) # Sample positions on x-axis [m]
	y = arange(0.0, ly + dy, dy) # Sample positions on y-axis [m]
	X, Y = meshgrid(x, y) # Create spatial grid
	Ii = zeros((size(X, 0),size(X, 1))) # Intensity distribution

	# Create support grid in the pupil plane for each lens
	xSup = arange(-supD/2,supD/2 + dx, dx)
	XSup, YSup = meshgrid(xSup, xSup) 	
	
	# Create spatial grid for the diffraction patterns for each lens
	dfft = lam*f/supD # Sample length [m]
	xfft = arange(-lam*f/2.0/dx, lam*f/2.0/dx + dfft, dfft) # Sample positions[m]
	Xfft,Yfft = meshgrid(xfft, xfft) # Create spatial grid
	
	# Create coordinates for the phase plates
	phPlateStx = lensCentx - D/2 # Start postions of each lenslet on x-axis [m]
	phPlateSty = lensCenty - D/2 # Start postions of each lenslet on y-axis [m]
	phPlateEndx = lensCentx + D/2 # End postions of each lenslet on x-axis [m]
	phPlateEndy = lensCenty + D/2 # End postions of each lenslet on y-axis [m]

	# Compute the intensity distribution on the image plane
	for ii in xrange(size(lensCentx)): # Run through lenslet array
		# Extract phase plate
		xPhase = arange(phPlateStx[ii],phPlateEndx[ii] + dx, dx) # Sample positions on x-axis [m]
		yPhase = arange(phPlateSty[ii],phPlateEndy[ii] + dy, dy) # Sample positions on y-axis [m]
		XPhase, YPhase = meshgrid(xPhase, yPhase) # Create spatial grid
		phaseInterp = interpolate.interp2d(x,y,phaseIn,kind='cubic') # Create interpolation function
		phasePlate = phaseInterp(xPhase,yPhase) # Create phase plate for individual lenslet		
		
		# Calculate the average phase tilt and preproces the phase plate
		Gx, Gy = gradient(phasePlate,dx,dy) # Determine the gradient of the phase plate
		Gx = mean(Gx) # Determine the tilt in the x-direction
		Gy = mean(Gy) # Determine the tilt in the y-direction
		theta = arctan(Gx/k) # Incident angle with respect to the x-axis [rad]
		phi = arctan(Gy/k) # Incident angle with respect to the y-axis [rad]
		xShift = tan(theta)*f # The spatial shift caused by the incident angle over the x-axis [m]
		yShift = tan(phi)*f # The spatial shift caused by the incident angle over the y-axis [m]
		phaseTilt = (Gx*XPhase + Gy*YPhase) # The phase that causes the tilt
		phasePlate = phasePlate - phaseTilt # Preprocessed phase plate
		
		# Calculate the pupil function and the fft
		P = sqrt(XSup**2.0 + YSup**2.0) <= D/2.0 # Pupil function
		phaseInterp = interpolate.interp2d(xPhase,yPhase,phasePlate,kind='cubic') # Create interpolation function
		phasePlate = phaseInterp(xSup,xSup) # Insert phase grid into the support grid
		Uin = exp(1j*phasePlate) # Caculate the complex amplitude from the phase 
		Ulb = P*Uin # Complex amplitude just before the lens
		Ula = dx*dy*numpy.fft.fftshift(numpy.fft.fft2(Ulb)) # Complex amplitude just behind the lens
		
		# Calculate the intensity distribution on the image plane
		Ui = exp(1j*k*f)*exp(1j*k/(2.0*f)*((Xfft + xShift)**2.0 + (Yfft + yShift)**2.0))/(1j*lam*f)*Ula # Complex amplitude on the image plane
		IiPlate = absolute(Ui)**2.0 # Intensity profile in the focal plane, numerically
		XfftPlate = Xfft + xShift + lensCentx[ii] # Adjust the x-axis
		YfftPlate = Yfft	+ yShift + lensCenty[ii] # Adjust the y-axis
		IiInterp = interpolate.interp2d(XfftPlate[0],YfftPlate[:,0],IiPlate,kind='cubic') # Create interpolation function
		IiPlate = IiInterp(x,y) # Insert support grid into the image plane grid
		Ii = Ii + IiPlate # Collect single lens patterns
	return X,Y,Ii