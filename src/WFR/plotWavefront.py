import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import numpy as np

def plotWavefront(Xpositions, Ypositions, phi, x_dim, y_dim, geometry):
	#title = "\phi(x), of the  reconstructed wavefront"
	#fig = p.figure();
	# Plot results in a surface plot
	#ax = p3.Axes3D(fig)
	#q = ax.scatter(Xpositions,Ypositions,phi, c=phi)
	#ax.set_xlabel('x')
	#ax.set_ylabel('y')
	#ax.set_zlabel(title)
	#fig.colorbar(q)
	#p.show()   
	
	z_min, z_max = phi.min(), phi.max()
	
	if geometry == 'fried':
		Xpositions = Xpositions.reshape((y_dim+1,x_dim+1))
		Ypositions = Ypositions.reshape((y_dim+1,x_dim+1))
		phi = phi.reshape((y_dim+1,x_dim+1))
	elif geometry == 'southwell':
		Xpositions = Xpositions.reshape((y_dim,x_dim))
		Ypositions = Ypositions.reshape((y_dim,x_dim))
		phi = phi.reshape((y_dim,x_dim))
	
	plt.figure()
	plt.scatter(Xpositions, Ypositions, c=phi)
	plt.colorbar()
	plt.show()
	
	#plt.figure()
	#plt.pcolormesh(Xpositions, Ypositions, phi, vmin=z_min, vmax=z_max)
	#plt.colorbar()
	#plt.show()
