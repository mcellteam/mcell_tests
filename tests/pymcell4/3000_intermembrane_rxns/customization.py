# This file hooks to override default MCell4 model
# code behavior for models generated from CellBlender
import mcell as m

import parameters

"""
def custom_argparse_and_parameters():
    # When uncommented, this function is called to parse 
    # custom commandline arguments.
    # It is executed before any of the automatically generated 
    # parameter values are set so one can override the parameter 
    # values here as well.
    pass
"""

"""
def custom_config(model):
    # When uncommented, this function is called to set custom
    # model configuration.
    # It is executed after basic parameter setup is done and 
    # before any components are added to the model. 
    pass
"""

def custom_init_and_run(model):
    
    A_plus_B = model.find_reaction_rule('A_plus_B')
    assert A_plus_B
    A_plus_B.is_intermembrane_surface_reaction = True

    model.initialize()
    
    if parameters.EXPORT_DATA_MODEL and model.viz_outputs:
        model.export_data_model()

    model.run_iterations(parameters.ITERATIONS)
    model.end_simulation()

