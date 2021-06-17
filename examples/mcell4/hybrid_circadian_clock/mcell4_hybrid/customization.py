# This file contains hooks to override default MCell4 model
# code behavior for models generated from CellBlender
import sys
import os
import shared
import mcell as m
import diffusion_constants

variant = ''

def custom_argparse_and_parameters():
    # When uncommented, this function is called to parse 
    # custom commandline arguments.
    # It is executed before any of the automatically generated 
    # parameter values are set so one can override the parameter 
    # values here as well.
    # To override parameter values, add or overwrite an item in dictionary
    # shared.parameter_overrides, e.g. shared.parameter_overrides['SEED'] = 10
    
    if len(sys.argv) != 4 or sys.argv[1] != '-seed':
        sys.exit("Expected following arguments: -seed N [D10_all|D1000_all|D10_prm_loc|D1000_prm_loc]") 
        
    # overwrite value of seed defined in module parameters
    shared.parameter_overrides['SEED'] = int(sys.argv[2])
    
    # and remember selected variant,
    # cannot use parameter_overrides because its values must be always floats
    global variant
    variant = sys.argv[3]


def custom_config(model):
    # When uncommented, this function is called to set custom
    # model configuration.
    # It is executed after basic parameter setup is done and 
    # before any components are added to the model. 

    print("Seting diffusion constants to variant " + variant)
    diffusion_constants.set_diffusion_constants(model, variant)


"""
def custom_init_and_run(model):
    # When uncommented, this function is called after all the model
    # components defined in CellBlender were added to the model.
    # It allows to add additional model components before initialization 
    # is done and then to customize how simulation is ran.
    # The module parameters must be imported locally otherwise     # changes to shared.parameter_overrides done elsewhere won't be applied.
    import parameters as parameters
    model.initialize()
    model.run_iterations(parameters.ITERATIONS)
    model.end_simulation()
"""

