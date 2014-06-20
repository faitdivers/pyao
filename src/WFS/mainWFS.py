#Lenslet Array
#Updated: Juni 11, 2014
import math
from numpy import *
from scipy import *
import numpy.fft
from scipy import interpolate


def wfs(phaseIn, paramsSensor):
	# Calculates the normalized intensity distribution on the detecor plane of the sensor	
	
	# Unwrap paramsSensor
	Nx = paramsSensor['numPupilx'] # Samples on the x-axis
	Ny = paramsSensor['numPupily'] # Samples on the y_axis
	lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
	ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
	lensCentx = paramsSensor['lensCentx'] # Normalized lenslet centers on x-axis
	lensCenty = paramsSensor['lensCenty'] # Normalized lenslet centers on y-axis
	lensCentx = lensCentx*lx # Lenslet centres [m]
	lensCenty = lensCenty*ly # Lenslet centres [m]
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
	Ii = zeros((size(y),size(x))) # Intensity distribution

	# Create support grid in the pupil plane for each lens
	xSup = arange(-supD/2,supD/2 + dx, dx) # Sample positions on x-axis [m]
	XSup, YSup = meshgrid(xSup, xSup) 	# Sample positions on y-axis [m]
	
	# Create spatial grid for the diffraction patterns for each lens
	dfft = lam*f/supD # Sample length [m]
	xfft = arange(-lam*f/2.0/dx, lam*f/2.0/dx + dfft, dfft) # Sample positions[m]
	
	# Calculate pupil function
	P = sqrt(XSup**2.0 + YSup**2.0) <= D/2.0 # Pupil function
	
	# Compute the intensity distribution on the image plane
	for ii in xrange(size(lensCentx)): # Run through lenslet array
		# Extract phase plate and get corresponding spatial coordinates
		phasePlate, xPhase, yPhase = extractPhasePlate(lensCentx[ii],
			lensCenty[ii], D, phaseIn, x, y, dx, dy)	
		
		# Calculate the average phase tilt and preproces the phase plate
		phasePlate, xShift, yShift = tiltPhasePlate(phasePlate, k, f, xPhase, yPhase, dx, dy)
		
		# Calculate the fft of the complex amplitude behind the lens
		phaseInterp = interpolate.interp2d(xPhase, yPhase, phasePlate, kind='cubic') # Create interpolation function
		phasePlate = phaseInterp(xSup, xSup) # Insert phase grid into the support grid
		Uin = exp(1j*phasePlate) # Caculate the complex amplitude from the phase 
		Ulb = P*Uin # Complex amplitude just before the lens
		Ui = dx*dy*numpy.fft.fftshift(numpy.fft.fft2(Ulb)) # Complex amplitude just behind the lens
		
		# Calculate the intensity distribution on the image plane
		IiPlate = absolute(Ui)**2.0 # Intensity profile in the focal plane, numerically
		xfftPlate = xfft + xShift + lensCentx[ii] # Adjust the x-axis
		yfftPlate = xfft	+ yShift + lensCenty[ii] # Adjust the y-axis
		IiInterp = interpolate.interp2d(xfftPlate, yfftPlate, IiPlate, kind='cubic') # Create interpolation function
		IiPlate = IiInterp(x, y) # Insert support grid into the image plane grid
		Ii = Ii + IiPlate # Collect single lens patterns
	Ii = Ii/amax(absolute(Ii)) # Normalize intensity distribution
	return x, y, Ii
 
	
def extractPhasePlate(lensCentx, lensCenty, D, phaseIn, x, y, dx, dy):
	# Extracts phase plate from the entire incident phase for calculation of a single lenslet	
	
     	# Create coordinates for the phase plates
	phPlateStx = lensCentx - D/2 # Start postions of each lenslet on x-axis [m]
	phPlateSty = lensCenty - D/2 # Start postions of each lenslet on y-axis [m]
	phPlateEndx = lensCentx + D/2 # End postions of each lenslet on x-axis [m]
	phPlateEndy = lensCenty + D/2 # End postions of each lenslet on y-axis [m]
 	
      # Extract phase plate
	xPhase = arange(phPlateStx,phPlateEndx + dx, dx) # Sample positions on x-axis [m]
	yPhase = arange(phPlateSty,phPlateEndy + dy, dy) # Sample positions on y-axis [m]
	phaseInterp = interpolate.interp2d(x,y,phaseIn,kind='cubic') # Create interpolation function
	phasePlate = phaseInterp(xPhase,yPhase) # Create phase plate for individual lenslet
	
	return phasePlate, xPhase, yPhase
	
	
def tiltPhasePlate(phasePlate, k, f, xPhase, yPhase, dx, dy):
	# Compesates tilt in the phase plate and gives the postion shifts for the diffraction pattern	
	
	# Calculate the average phase tilt and preproces the phase plate
	Gy, Gx = gradient(phasePlate,dy,dx) # Determine the gradient of the phase plate
	Gx = mean(Gx) # Determine the tilt in the x-direction
	Gy = mean(Gy) # Determine the tilt in the y-direction
	theta = arctan(Gx/k) # Incident angle with respect to the x-axis [rad]
	phi = arctan(Gy/k) # Incident angle with respect to the y-axis [rad]
	xShift = tan(theta)*f # The spatial shift caused by the incident angle over the x-axis [m]
	yShift = tan(phi)*f # The spatial shift caused by the incident angle over the y-axis [m]
	XPhase, YPhase = meshgrid(xPhase, yPhase) # Create spatial grid
	phaseTilt = (Gx*XPhase + Gy*YPhase) # The phase that causes the tilt
	phasePlate = phasePlate - phaseTilt # Preprocessed phase plate
	
	return phasePlate, xShift, yShift