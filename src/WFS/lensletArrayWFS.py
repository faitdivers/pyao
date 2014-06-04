#Current Status for Single Lens System May 19, 2014
import math
from numpy import *
from scipy import *
import numpy.fft
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate

paramsSensor = {
	# Number of samples in the pupil plane per lenslet
	'Nx' : 20.0,
	'Ny' : 20.0,
	# The lenslet configuration
	'lensletConfig' : array([[1, 1, 1, 1, 1],
					  [1, 1, 1, 1, 1],
					  [1, 1, 1, 1, 1],
					  [1, 1, 1, 1, 1],																					
					  [1, 1, 1, 1, 1]]),
	# Focal Length [m]
	'f' : 18.0e-3,
	# Diameter of aperture of single lenslet [m]	
	'D' : 300.0e-6, 
	# Wavelength [m]	
	'lam' : 630.0e-9, 	
	# Distance between lenslets [m]	
	'dl' : 10.0e-6,	
	}
	
def createTestPhase(paramsSensor):
	# Unwrap paramsSensor
	NxLens = paramsSensor['Nx'] # Samples on the x-axis per lenslet
	NyLens = paramsSensor['Ny'] # Samples on the y_axis per lenslet
	lensletConfig = paramsSensor['lensletConfig'] # Lenslet configuration
	D = paramsSensor['D'] # Lens diameter [m]
	lam = paramsSensor['lam'] # Wavelength [m]
	dl = paramsSensor['dl'] # Distance between lenslets [m]
	k = 2*pi/lam # Wavenumber
	nx = size(lensletConfig,1) # Number of lenslets in the x-direction
	ny = size(lensletConfig,0) # Number of lenslets in the y-direction
	Nx = NxLens*nx # Total number of samples on x-axis
	Ny = NyLens*ny # Total number of samples on y-axis
	lx = (nx - 1.0)*(dl + D) + D # Length of array in x-direction [m]
	ly = (ny - 1.0)*(dl + D) + D # Length of array in y-direction [m]
	dxo = lx/(Nx - 1.0) # Sample length on x-axis [m]
	dyo = ly/(Ny - 1.0) # Sample length on y-axis [m]
	xo = arange(0.0,lx + dxo,dxo) # Sample positions on x-axis [m]
	yo = arange(0.0,ly + dxo,dyo) # Sample positions on y-axis [m]
	Xo, Yo = meshgrid(xo,yo) # Create spatial grid

	ax = random.uniform(-1.0,1.0)*2.0
	ay = random.uniform(-1.0,1.0)*2.0
	bx = random.uniform(-1.0,1.0)*1.0
	by = random.uniform(-1.0,1.0)*1.0
	cx = random.uniform(-1.0,1.0)*0.0001 # Tilt x
	cy = random.uniform(-1.0,1.0)*0.0001 # Tilt y
	ex = random.uniform(-1.0,1.0)*2.0
	ey = random.uniform(-1.0,1.0)*2.0
	d =  random.uniform(-1.0,1.0)

	phaseIn = k*((ax*Xo)**3.0 + (ay*Yo)**3.0 + (bx*Xo)**2.0 + 
		(by*Yo)**2.0 + cx*Xo + cy*Yo + d + (ex*Xo)**4.0 + (ey*Yo)**4.0)
	
	return Xo,Yo,phaseIn

def lensletArray(phaseIn, paramsSensor):
	# Unwrap paramsSensor
	NxLens = paramsSensor['Nx'] # Samples on the x-axis per lenslet
	NyLens = paramsSensor['Ny'] # Samples on the y_axis per lenslet
	lensletConfig = paramsSensor['lensletConfig'] # Lenslet configuration
	f = paramsSensor['f'] # Focal length [m]
	D = paramsSensor['D'] # Lens diameter [m]
	lam = paramsSensor['lam'] # Wavelength [m]
	dl = paramsSensor['dl'] # Distance between lenslets [m]
	k = 2*pi/lam # Wavenumber
		
	# Lenslet configuration parameters
	nx = size(lensletConfig,1) # Number of lenslets in the x-direction
	ny = size(lensletConfig,0) # Number of lenslets in the y-direction
	lensCentx = arange(nx)*(dl + D) + D/2 # Centers on x-axis [m]
	lensCenty = arange(ny)*(dl + D) + D/2 # Centers on y-axis [m]
	Nx = NxLens*nx # Total number of samples on x-axis
	Ny = NyLens*ny # Total number of samples on y-axis
	lx = (nx - 1.0)*(dl + D) + D # Length of array in x-direction [m]
	ly = (ny - 1.0)*(dl + D) + D # Length of array in y-direction [m]
	
	# Create grid in the pupil plane
	dxo = lx/(Nx - 1.0) # Sample length on x-axis [m]
	dyo = ly/(Ny - 1.0) # Sample length on y-axis [m]
	xo = arange(0.0,lx + dxo,dxo) # Sample positions on x-axis [m]
	yo = arange(0.0,ly + dxo,dyo) # Sample positions on y-axis [m]
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
	dxi = dfx*lam*f # Sample length on x-axis [m]
	dyi = dfx*lam*f # Sample length on y-axis [m]
	xi = arange(0.0,lx + dxi,dxi) # Sample positions on x-axis [m]
	yi = arange(0.0,ly + dyi,dyi) # Sample positions on y-axis [m]
	Xi, Yi = meshgrid(xi,yi) # Create spatial grid
	Ii = 	zeros((size(Xi,0),size(Xi,1))) # Intensity distribution
	
	# Create coordinates for the phase plates
	phPlateStx = arange(nx)*(dl + D) # Start postions of each lenslet on x-axis [m]
	phPlateSty = arange(ny)*(dl + D) # Start postions of each lenslet on y-axis [m]
	phPlateEndx = arange(nx)*(dl + D) + D # End postions of each lenslet on x-axis [m]
	phPlateEndy = arange(ny)*(dl + D) + D # End postions of each lenslet on y-axis [m]

	# Compute the intensity distribution on the image plane
	tol = 1.0e-10 # Tolerance on equal function
	for yy in xrange(ny): # y-direction
		for xx in xrange(nx): # x-direction
			if lensletConfig[yy,xx] == 0: # Skip lenslet if true
				continue

			# Extract phase plate
			indStx = where((xo > phPlateStx[xx]) + (absolute(xo - phPlateStx[xx]) < tol))[0][0]
			indSty = where((yo > phPlateSty[yy]) + (absolute(yo - phPlateSty[yy]) < tol))[0][0]
			indEndx = where((xo > phPlateEndx[xx]) + (absolute(xo - phPlateEndx[xx]) < tol))[0][0]
			indEndy = where((yo > phPlateEndy[yy]) + (absolute(yo - phPlateEndy[yy]) < tol))[0][0]
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
			Xifft = Fx*lam*f + xShift + lensCentx[xx] # Adjust the x-axis
			Yifft = Fy*lam*f	+ yShift + lensCenty[yy] # Adjust the y-axis
			IiIntpF = interpolate.interp2d(Xifft[0],Yifft[:,0],IiTemp) # Create interpolation function
			IiTemp = IiIntpF(xi,yi) # Insert single pattern grid into the whole image plane grid
			Ii = Ii + IiTemp # Collect single lens patterns
	return Xi,Yi,Ii
	
Xo,Yo,phaseIn = createTestPhase(paramsSensor)

figPhaseIn = pl.figure()
ax = figPhaseIn.gca(projection='3d')
surf = ax.plot_surface(Xo,Yo,phaseIn, rstride=1, cstride=1, cmap='jet')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Phase')
pl.show()

Xi,Yi,Ii = lensletArray(phaseIn, paramsSensor)

Ximm = Xi*1000.0
Yimm = Yi*1000.0
figIi = pl.figure()
conNum = pl.pcolor(Ximm,Yimm,Ii)
pl.title('Numerical Solution (mm)')
pl.show()
