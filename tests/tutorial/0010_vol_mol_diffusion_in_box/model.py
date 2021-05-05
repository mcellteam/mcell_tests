"""
0010
In this tutorial, we will start from 0000_vol_mol_diffusion/model.py and
add a box that reflects molecules.
We will also export the geometry so the model can be visualized in 
CellBlender directly just using information provided in this 
model file. 

All the explanations from the previous version are removed and 
only their code is being kept for reference. 
The new code blocks and explanations are marked with index 0010-X.  
"""

#0000-1) 
import sys
import os


#0000-2)
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    sys.path.append(lib_path)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)
    
    
#0000-3)
import mcell as m
    
    
#0000-4)
species_a = m.Species(
    name = 'a', 
    diffusion_constant_3d = 1e-6
)


#0000-5)
release_site_a = m.ReleaseSite(
    name = 'rel_a', 
    complex = species_a, 
    location=(0, 0, 0), 
    number_to_release = 1
)


#0000-6)
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00000/Scene',
)


"""
0010-1)
The main difference from our previous tutorial is 
that we will create a geometry object in the shape of a cube.
Geometry objects are defined using a list of vertices and 
a list of walls.

The easiest way how to create definitions of more complex 
objects is to create a CellBlender model and export it
through Run Simulation -> Export & Run, and then 
use the generated definition in file <project base name>_geometry.py 
located in directory 
<.blend file location>/<project_name>_files/mcell/output_data/.

In this tutorial, we can use this prepared object definition.

The box_vertex_list contains triplets of x, y, z coordinates 
and uses um (micrometer) units.
"""
box_vertex_list = [
    [-0.125, -0.125, -0.125],   # 0
    [-0.125, -0.125, 0.125],    # 1
    [-0.125, 0.125, -0.125],    # 2
    [-0.125, 0.125, 0.125],     # 3
    [0.125, -0.125, -0.125],    # 4
    [0.125, -0.125, 0.125],     # 5
    [0.125, 0.125, -0.125],     # 6
    [0.125, 0.125, 0.125]       # 7
] 


"""
0010-2)
A wall is a triangle in 3D space and it is defined using 
three vertices. 
"""
box_wall_list = [
    # [1, 2, 0] defines a triangle connecting vertices 
    # [-0.125, -0.125, 0.125], [-0.125, 0.125, -0.125], and
    # [-0.125, -0.125, -0.125]
    [1, 2, 0],  
    [3, 6, 2], 
    [7, 4, 6], 
    [5, 0, 4], 
    [6, 0, 2], 
    [3, 5, 7], 
    [1, 3, 2], 
    [3, 7, 6], 
    [7, 5, 4], 
    [5, 1, 0], 
    [6, 4, 0], 
    [3, 1, 5]
] 


"""
0010-3)
We use the previously defined list of vertices and walls 
to create an object of class GeometryObject.
"""
box = m.GeometryObject(
    name = 'box',
    vertex_list = box_vertex_list,
    wall_list = box_wall_list
)

    
#0000-7)
model = m.Model()
model.add_species(species_a)
model.add_release_site(release_site_a)
model.add_viz_output(viz_output)


"""
0010-4)
In addition to the previous components, we also add our box 
to the model.
"""
model.add_geometry_object(box)


#0000-8)
model.initialize()

"""
0010-5)
In the previous tutorial model 0000, there was a prepared 
CellBlender project file viz.blend file used to visualize
the simulation. Since the model including its geometry 
is defined by the Python code, we need a way how to export 
this information so that Blender or other tools can read and 
display it.
"""
model.export_geometry_as_obj()

"""
0010-6)
Now lets run the simulation for 100 iterations. 
"""
model.run_iterations(100)
model.end_simulation()


#0000-9)
"""
0010-7)
Open a terminal (command line), change the current directory 
to the directory where this file is stored and run:

> python model.py

Information on the progress of simulation and
final statistics are printed.
We can now take a look at the visualization output files. 
   
Under directory viz_data/seed_00000/, there are
files Scene.ascii.0000000.dat - Scene.ascii.0000010.dat
that contain location of the molecule.   

The format of visyalization data is:
species_name id x y z nx ny nz
 
Where x,y,z is the location (in um) and nx,ny,nz is the normal vector 
that is always 0,0,0 for volume molecules. 

The first location right after release is in Scene.ascii.0000000.dat:
a 0 0 0 0 0 0 0

And the final location is in Scene.ascii.0000010.dat:
a 0 -0.00204423885 0.0107041633 -0.0267571038 0 0 0
(the actual positions may differ)
"""


"""
0000-10)
We can also use CellBlender to visualize the trajectory. 
To do this:
1) start CellBlender with ./my_blender or blender.exe,
2) open file viz.blend (in the same directory as this script),
3) select panel Visualization Settings,
4) click on Read Viz Data and navigate to directory viz_data/seed_00000/,
5) click on Play Animation button (Triangle aiming to the left) 
   on the middle bottom of the CellBlender window.
   
You should see how the molecule diffuses around during the 
10 iterations.

This concludes the first section of the MCell4 Python tutorial
where we created a model that releases a single molecule and 
simulates its diffusion.
"""    
