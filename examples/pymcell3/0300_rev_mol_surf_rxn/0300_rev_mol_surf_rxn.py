#!/usr/bin/env python3

# TODO: this is probably not the way how the inport form a different directory should be done
import os
import sys
MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
	sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
	print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")

import time

import pymcell as m

if __name__ == "__main__":

	tetrahedron_vert_list = [
		[  0.00,  0.00,  0.02 ],
		[  0.02,  0.00, -0.01 ],
		[ -0.01,  0.02, -0.01 ],
		[ -0.01, -0.02, -0.01 ]
	]

	tetrahedron_face_list = [
		[ 0, 1, 2 ],
		[ 0, 2, 3 ],
		[ 0, 3, 1 ],
		[ 1, 3, 2 ]
	]

	seed = 1

	world = m.mcell_create()
	m.mcell_set_seed(world,seed)
	m.mcell_init_state(world)

	# Timestep, iters
	m.mcell_set_time_step(world, 0.1)
	m.mcell_set_iterations(world, 10)

	# Create a scene
	scene_name = "Scene"
	scene = m.create_instance_object(world, scene_name)

	# add geometry object with defined regions
	box_name = 'Tetrahedron'
	box_obj = m.create_polygon_object(world, tetrahedron_vert_list, tetrahedron_face_list, scene, box_name)

	# Define volume molecules species
	species_vol = m.create_species(world, "A", 0, False)
	species_vol2 = m.create_species(world, "A2", 0, False)

	# Define surface molecule
	species_surf = m.create_species(world, "B", 0, True)
	species_surf2 = m.create_species(world, "B2", 0, True)

	###############################################################################
	###############################################################################
	#   Vol + Vol -> Vol       THIS WORKS
	###############################################################################
	###############################################################################

	'''
	r_spec_list = None
	r_spec_list = m.mcell_add_to_species_list(
		species_vol, False, 0, r_spec_list)
	r_spec_list = m.mcell_add_to_species_list(
		species_vol, False, 0, r_spec_list)

	p_spec_list = None
	p_spec_list = m.mcell_add_to_species_list(
		species_vol, False, 0, p_spec_list)

	m.create_reaction(
		world=world,
		reactants=r_spec_list,
		products=p_spec_list,
		rate_constant=1.0
		)
	'''

	###############################################################################
	###############################################################################
	#   Vol + Vol <-> Vol       THIS WORKS
	###############################################################################
	###############################################################################

	'''
	r_spec_list = None
	r_spec_list = m.mcell_add_to_species_list(
		species_vol, False, 0, r_spec_list)
	r_spec_list = m.mcell_add_to_species_list(
		species_vol, False, 0, r_spec_list)

	p_spec_list = None
	p_spec_list = m.mcell_add_to_species_list(
		species_vol, False, 0, p_spec_list)

	m.create_reaction(
		world=world,
		reactants=r_spec_list,
		products=p_spec_list,
		rate_constant=1.0,
		backward_rate_constant=0.5
		)
	'''

	###############################################################################
	###############################################################################
	#   Vol + Surf -> Vol       THIS WORKS
	###############################################################################
	###############################################################################

	'''
	r_spec_list = None
	r_spec_list = m.mcell_add_to_species_list(
		species_vol, True, 1, r_spec_list) # 1 = up
	r_spec_list = m.mcell_add_to_species_list(
		species_surf, True, 1, r_spec_list) # 1 = up

	p_spec_list = None
	p_spec_list = m.mcell_add_to_species_list(
		species_vol, True, 1, p_spec_list) # 1 = up

	m.create_reaction(
		world=world,
		reactants=r_spec_list,
		products=p_spec_list,
		rate_constant=1.0
		)
	'''

	###############################################################################
	###############################################################################
	#   Vol + Surf <-> Vol       THIS FAILS
	###############################################################################
	###############################################################################

	r_spec_list = None
	r_spec_list = m.mcell_add_to_species_list(
		species_vol, True, 1, r_spec_list) # 1 = up
	r_spec_list = m.mcell_add_to_species_list(
		species_surf, True, 1, r_spec_list) # 1 = up

	p_spec_list = None
	p_spec_list = m.mcell_add_to_species_list(
		species_vol2, True, 1, p_spec_list) # 1 = up
	p_spec_list = m.mcell_add_to_species_list(
		species_surf2, True, 1, p_spec_list) # 1 = up

	m.create_reaction(
		world=world,
		reactants=r_spec_list,
		products=p_spec_list,
		rate_constant=1.0,
		backward_rate_constant=0.3
		)

	###############################################################################
	###############################################################################
	#   Run
	###############################################################################
	###############################################################################

	m.mcell_init_simulation(world)
	m.mcell_init_output(world)

	for i in range(5):
		m.mcell_run_iteration(world, 1, 0)
	m.mcell_flush_data(world)
	m.mcell_print_final_warnings(world)
	m.mcell_print_final_statistics(world)
