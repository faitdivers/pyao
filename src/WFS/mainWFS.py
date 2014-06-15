#Lenslet Array
#Updated: Juni 2, 2014
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
	k = 2*pi/lam # Wavenumber
	
	# Create grid in the pupil plane
	dxo = lx/(Nx - 1.0) # Sample length on x-axis [m]
	dyo = ly/(Ny - 1.0) # Sample length on y-axis [m]
	xo = arange(0.0,lx + dxo,dxo) # Sample positions on x-axis [m]
	yo = arange(0.0,ly + dyo,dyo) # Sample positions on y-axis [m]
	Xo, Yo = meshgrid(xo,yo) # Create spatial grid

	# Create grid for the Fast Fourier Transform (fft)
	Lx = dxo*Nx # Support length for the fft over the x-axis [m]
	Ly = dyo*Ny # Support length for the fft over the y-axis [m]
	xfft = arange(-Lx/2.0,Lx/2.0,dxo) # Sample positions on x-axis [m]
	yfft = arange(-Ly/2.0,Ly/2.0,dyo) # Sample positions on y-axis [m]
	Xfft,Yfft = meshgrid(xfft,yfft) # Create spatial grid
	dfx = 1.0/Lx # Sample frequency on fx-axis [rad/m]
	dfy = 1.0/Ly # Sample frequency on fy-axis [rad/m]
	fx = arange(-1.0/2.0/dxo,1.0/2.0/dxo,dfx) # Spatial frequency positions on fx-axis [rad/m]
	fy = arange(-1.0/2.0/dyo,1.0/2.0/dyo,dfy) # Spatial frequency positions on fy-axis [rad/m]
	Fx, Fy = meshgrid(fx,fy) # Create spatial frequency grid [rad/m]
	
	# Create grid in the image plane
	# Sampling based on the sensor parameters
	dxi = lx/(Nx - 1.0) # Sample length on x-axis [m]
	dyi = ly/(Ny - 1.0) # Sample length on y-axis [m]
	xi = arange(0.0,lx + dxi,dxi) # Sample positions on x-axis [m]
	yi = arange(0.0,ly + dyi,dyi) # Sample positions on y-axis [m]
	Xi, Yi = meshgrid(xi,yi) # Create spatial grid
	Ii = zeros((size(Xi,0),size(Xi,1))) # Intensity distribution	
	
	# Create coordinates for the phase plates
	phPlateStx = lensCentx - D/2 # Start postions of each lenslet on x-axis [m]
	phPlateSty = lensCenty - D/2 # Start postions of each lenslet on y-axis [m]
	phPlateEndx = lensCentx + D/2 # End postions of each lenslet on x-axis [m]
	phPlateEndy = lensCenty + D/2 # End postions of each lenslet on y-axis [m]

	# Compute the intensity distribution on the image plane
	tol = 1.0e-10 # Tolerance on equal function
	for ii in xrange(size(lensCentx)): # Run through lenslet array
		# Extract phase plate
		indStx = where((xo > phPlateStx[ii]) + (absolute(xo - phPlateStx[ii]) < tol))[0][0]
		indSty = where((yo > phPlateSty[ii]) + (absolute(yo - phPlateSty[ii]) < tol))[0][0]
		indEndx = where((xo > phPlateEndx[ii]) + (absolute(xo - phPlateEndx[ii]) < tol))[0][0]
		indEndy = where((yo > phPlateEndy[ii]) + (absolute(yo - phPlateEndy[ii]) < tol))[0][0]
		phaseInfft = phaseIn[indSty:indEndy,indStx:indEndx] # Extracted phase plate
		
		# Create temporary spatial grid for the phase plate
		NxTemp = size(phaseInfft,1) 
		NyTemp = size(phaseInfft,0)
		xfftTemp = arange(-NxTemp*dxo/2.0,NxTemp*dxo/2.0,dxo)
		xfftTemp = xfftTemp[0:NxTemp]
		yfftTemp = arange(-NyTemp*dyo/2.0,NyTemp*dyo/2.0,dyo)
		yfftTemp = yfftTemp[0:NyTemp]
		XfftTemp, YfftTemp = meshgrid(xfftTemp,yfftTemp)
		
		# Calculate the average phase tilt and preproces the phase plate
		Gx, Gy = gradient(phaseInfft,dxo,dyo) # Determine the gradient of the phase plate
		Gx = mean(Gx) # Determine the tilt in the x-direction
		Gy = mean(Gy) # Determine the tilt in the y-direction
		theta = arctan(Gx/k) # Incident angle with respect to the x-axis [rad]
		phi = arctan(Gy/k) # Incident angle with respect to the y-axis [rad]
		xShift = tan(theta)*f # The spatial shift caused by the incident angle over the x-axis [m]
		yShift = tan(phi)*f # The spatial shift caused by the incident angle over the y-axis [m]
		phaseTilt = (Gx*XfftTemp + Gy*YfftTemp) # The phase that causes the tilt
		phaseInfft = phaseInfft - phaseTilt # Preprocessed phase plate
		
		# Calculate the pupil function and the fft
		P = sqrt(Xfft**2.0 + Yfft**2.0) <= D/2.0	# Pupil function
		phIntpF = interpolate.interp2d(XfftTemp[0],YfftTemp[:,0],phaseInfft,kind='linear') # Create interpolation function
		phaseInfft = phIntpF(xfft,yfft) # Insert phase grid into the support grid
		Uin = exp(1j*phaseInfft) # Caculate the complex amplitude from the phase 
		Ulb = P*Uin # Complex amplitude just before the lens
		Ula = dxo*dyo*numpy.fft.fftshift(numpy.fft.fft2(Ulb)) # Complex amplitude just behind the lens
		
		# Calculate the intensity distribution on the image plane
		fxShift = xShift/(lam*f) # Shift in spatial frequency fx-axis [rad/m]
		fyShift = yShift/(lam*f) # Shift in spatial frequency fy-axis [rad/m]
		Fx = Fx[0:size(Ula,0),0:size(Ula,1)]
		Fy = Fy[0:size(Ula,0),0:size(Ula,1)]
		Ui = exp(1j*k*f)*exp(1j*k*((Fx + fxShift)**2 + (Fy + fyShift)**2)*lam**2*f/2)/(1j*lam*f)*Ula # Complex amplitude on the image plane
		IiTemp = absolute(Ui)**2.0 # Intensity profile in the focal plane, numerically
		Xifft = Fx*lam*f + xShift + lensCentx[ii] # Adjust the x-axis
		Yifft = Fy*lam*f	+ yShift + lensCenty[ii] # Adjust the y-axis
		IiIntpF = interpolate.interp2d(Xifft[0],Yifft[:,0],IiTemp,kind='cubic') # Create interpolation function
		IiTemp = IiIntpF(xi,yi) # Insert single pattern grid into the whole image plane grid
		Ii = Ii + IiTemp # Collect single lens patterns
	return Xi,Yi,Ii