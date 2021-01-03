

def custom_init_and_run(model):
    model.initialize()

    model.run_iterations(1)
    
    print("*** SAVE ***")
    model.save_checkpoint()
    
    #model.run_iterations(parameters.ITERATIONS)
    
    model.end_simulation()