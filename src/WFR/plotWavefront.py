import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt

def plotWavefront(Xpositions, Ypositions, phi):
	title = "\phi(x), of the  reconstructed wavefront"
	# Plot results in a surface plot
	fig = p.figure();
	ax = p3.Axes3D(fig)
	q = ax.scatter(Xpositions,Ypositions,phi, c=phi)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel(title)
	fig.colorbar(q)
	p.show()   
	
	plt.figure()
	plt.scatter(Xpositions, Ypositions, c=phi)
	plt.colorbar()
	plt.show()
