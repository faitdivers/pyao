import numpy as np


def calculate_hmatrix(actuator_parameters, reconstruction_parameters):
	"""
	
	"""
	sig1 = actuator_parameters['sig1']
	sig2 = actuator_parameters['sig2']
	w1 = actuator_parameters['w1']
	w2 = actuator_parameters['w2']
	num_act_x = actuator_parameters['numActx']
	num_act_y = actuator_parameters['numActy']
	act_distance = actuator_parameters['act_distance']
	
	act_pos_x, act_pos_y = calculate_dm_square_configuration(num_act_x, num_act_y, act_distance)
	number_of_actuators = len(act_pos_x)
	
	phi_positions_x = reconstruction_parameters['phi_positions_x']
	phi_positions_y = reconstruction_parameters['phi_positions_y']
	number_of_phi_locations = len(phi_positions_x)
	
	H = np.zeros([number_of_phi_locations, number_of_actuators])
	
	k1 = w1 / (2 * np.pi * sig1 ** 2)
	k2 = w2 / (2 * np.pi * sig2 ** 2)

	for i in range(0, number_of_phi_locations):
		for j in range(0, number_of_actuators):
			y_squared = (phi_positions_y[i] - act_pos_y[j]) ** 2
			x_squared = (phi_positions_x[i] - act_pos_x[j]) ** 2
			y_sqrd_x_sqrd = y_squared + x_squared
			
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


def calculate_dm_wavefront(control_command, h_matrix):
	"""

	"""
	dm_wavefront = np.dot(h_matrix, control_command)
	return dm_wavefront


def calculate_dm_square_configuration(num_act_x, num_act_y, distance_actuators):
	"""

	"""
	act_cent_x = np.arange(num_act_x) * distance_actuators + (distance_actuators / 2)
	act_cent_y = np.arange(num_act_y) * distance_actuators + (distance_actuators / 2)
	act_cent_x, act_cent_y = np.meshgrid(act_cent_x, act_cent_y) # Create rectangular grids for centres [m]
	act_cent_x = np.hstack(act_cent_x) # Stack the rectangular grids [m]
	act_cent_x = np.hstack(act_cent_y) # Stack the rectangular grids [m]
	
	return act_cent_x, act_cent_y


def dm(actCom, paramsSens):
	return np.zeros((paramsSens['numPupilx'],paramsSens['numPupily']))

