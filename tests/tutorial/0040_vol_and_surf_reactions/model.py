"""
0040
In this tutorial section, we will continue with the model 
we created in section 0030_mol_release_with_bngl_and_compartments,
add one more sphere representing a cell and
define a transport and volume-volume reactions.  
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
    

#0000-6)
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00001/Scene',
)


#0020-1)
organelle_1 = m.geometry_utils.create_icosphere(
    name = 'Organelle_1', 
    radius = 0.3, 
    subdivisions = 4
)


#0020-2)
organelle_1.translate((0, -0.2, 0))


#0030-1)
cell = m.geometry_utils.create_icosphere(
    name = 'Cell', 
    radius = 0.6, 
    subdivisions = 4
)


"""
0040-1)
We will define new species and also define releases of these molecules. 
Open file 'model.bngl' and follow the tutorial present in this 
directory's file called also model.bngl.
"""

#0000-7)
model = m.Model()
model.add_viz_output(viz_output)


#0020-2)
model.add_geometry_object(organelle_1)


#0030-11)
model.add_geometry_object(cell)


#0030-6)
"""
0040-10)
Associate geometry objects with BNGL compartments.
For 3D (volume) compartments the name of the geopmetry object is 
used as the compartment name. To match the 2D (surface) compartment 
name, we must specify it explicitly.  
"""
organelle_1.is_bngl_compartment = True
organelle_1.surface_compartment_name = 'Organelle_1_surface'

cell.is_bngl_compartment = True


#0030-7)
"""
0040-11)
Load the BNGL file located in the same directory as this Python script. 
"""
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))
model.load_bngl(os.path.join(MODEL_PATH, 'model.bngl')) 


#0000-8)
model.initialize()


#0010-5)
model.export_viz_data_model()


#0010-6)
model.run_iterations(100)
model.end_simulation()


"""
0040-12)
Run the model:

> python model.py
"""

"""
0040-13)
And visualize it:

$MCELL_PATH/utils/visualize.sh viz_data/seed_00001/

Play the visualization animation. 
Molecules t1 are diffuse on the surface of Organelle_1.
Whe you jump to iteration around 100 you can notice that 
there are a few molecules of different color inside of the 
Organelle_1 object. Those are the molecules 'c' created 
when 'a' and 'b' react.


In this section, we introduced surface molecules, 
compartments hieararchy, and also volume-volume and 
volume-surface reactions. 
"""    
