"""
0050
In this tutorial section, we will continue with the model 
we created in section 0040_vol_and_surf_reactions,
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
0050-1)
We will define observables using the BioNetGen language. 
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
#0040-10)
organelle_1.is_bngl_compartment = True
organelle_1.surface_compartment_name = 'Organelle_1_surface'

cell.is_bngl_compartment = True


#0030-7)
#0040-11)
"""
#0050-3)
In the previous tutorial sections, the only argument we needed to 
pass was the path to the BNGL file. 
Now we would also line to specify directory for the output 
files where the counts of observables will be stored. 
The default is the current directory and we will chaneg it to a more 
common directory react_data with subdirectory that contains the 
seed value (1 in our case). 
"""
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))
model.load_bngl(
    file_name = os.path.join(MODEL_PATH, 'model.bngl'),
    observables_files_prefix = './react_data/seed_00001/'
)    



#0000-8)
model.initialize()


#0010-5)
model.export_viz_data_model()


#0010-6)
model.run_iterations(100)
model.end_simulation()


"""
0050-4)
Run the model:

> python model.py
"""

"""
0050-5)
We visualized the model in the previous tutorial section, so we will 
look just at the observable counts. 
Navigate to the directory react_data/seed_00001/ and 
open for instance the file a.dat created from BNGL observable 
defined as:
  Molecules a a 

The first column is time (in seconds) and the second value is the
count of molecules matching pattern 'a'.  

0 1000
1e-06 1000
...
9e-06 999
1e-05 999
...

There are many ways how to visualize the .dat files,
a utility python script is provided with MCell.
To use it to display the data, run the script below 
with argument pointing to the directory with our observable files: 

> python $MCELL_PATH/utils/plot_single_run.py react_data/seed_00001/

We ran the simulation just for 100 iterations (100 us because 
the default tiem step is 1 us), so no big changes are 
happening. Still, one can see that the number of molecules
'a' in organelle_1 grows and as they react with 'b'
the number of 'c' grows as well.  
You can try to run the simulation for longer, e.g. 1000 for 
iterations and check the counts of molecules afterwards.  


In this section, we introduced BNGL observables that allow 
to count how the numbers of molecules change over time in 
specified compartments.
"""    
