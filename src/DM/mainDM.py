import numpy as np


def calculate_hmatrix(actuator_parameters, reconstructed_wavefront):
	"""
	
	"""
	sig1 = actuator_parameters['sig1']
	sig2 = actuator_parameters['sig2']
	w1 = actuator_parameters['w1']
	w2 = actuator_parameters['w2']
	actuator_positions_x = actuator_parameters['actuator_positions_x']
	actuator_positions_y = actuator_parameters['actuator_positions_y']
	number_of_actuators = len(actuator_positions_x)
	
	phi_locations_x = reconstructed_wavefront[0]
	phi_locations_y = reconstructed_wavefront[1]
	number_of_phi_locations = len(phi_locations_x)
	
	H = np.zeros([number_of_phi_locations, number_of_actuators])
	
	k1 = w1 / (2 * np.pi * sig1 ** 2)
	k2 = w2 / (2 * np.pi * sig2 ** 2)

	for i in range(0, number_of_phi_locations):
		for j in range(0, number_of_actuators):
			y_sqrd = (phi_locations_y[i] - actuator_positions_y[j]) ** 2
			x_srqd = (phi_locations_x[i] - actuator_positions_x[j]) ** 2
			y_sqrd_x_sqrd = y_sqrd + x_srqd
			
			part1 = k1 * np.exp(- y_sqrd_x_sqrd / (2 * sig1 ** 2))
			part2 = k2 * np.exp(- y_sqrd_x_sqrd / (2 * sig2 ** 2))
			
			H[i][j] = part1 + part2
	return H


def calculate_actuation_command(reconstructed_wavefront, h_matrix):
	"""

	"""
	p1 = np.dot(h_matrix.T, h_matrix)
	p1_inv = np.linalg.inv(p1)
	p2 = np.dot(p1_inv, h_matrix.T)
	u = np.dot(p2, reconstructed_wavefront)
	return u


def dm(actCom, paramsSens):
	return zeros((paramsSens['numPupilx'],paramsSens['numPupily']))

