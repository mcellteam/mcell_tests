import sys
import os


MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    sys.path.append(lib_path)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)
    
    
import mcell as m
    
viz_output = m.VizOutput(
    output_files_prefix = './viz_data/seed_00000/Scene',
)

box1 = m.geometry_utils.create_box('box1', 0.25)
box2 = m.geometry_utils.create_box('box2', 0.5)
box3 = m.geometry_utils.create_box('box3', 1)

model = m.Model()
model.add_geometry_object(box1)
model.add_geometry_object(box2)
model.add_geometry_object(box3)


model.initialize()

model.export_geometry("geometry")

model.end_simulation()

# check outputs