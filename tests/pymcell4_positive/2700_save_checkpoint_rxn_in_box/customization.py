
import os
import sys
import subprocess


def files_are_same(f1, f2, skip_n_lines_in_f1 = 0):
    with open(f1, 'r') as fin1:
        with open(f2, 'r') as fin2:
            for i in range(skip_n_lines_in_f1):
                fin1.readline()
            
            for line in fin1:
                assert line == fin2.readline()


def custom_init_and_run(model):
    model.initialize()

    model.run_iterations(5)
    
    model.save_checkpoint()
    
    model.run_iterations(5)
    
    model.end_simulation()
    
    # run the saved checkpoint and compare viz outputs
    print("Running checkpointed model")
    
    dir = os.path.join('checkpoints', 'seed_00001', 'it_05')
    subprocess.run([sys.executable, 'model.py'], cwd=dir, check=True)
    
    # compare outputs - both viz and react data
    viz_dir = os.path.join('viz_data', 'seed_00001')
    react_dir = os.path.join('react_data', 'seed_00001')
    
    files_are_same(os.path.join(viz_dir, 'Scene.ascii.05.dat'), os.path.join(dir, viz_dir, 'Scene.ascii.05.dat')) 
    files_are_same(os.path.join(viz_dir, 'Scene.ascii.10.dat'), os.path.join(dir, viz_dir, 'Scene.ascii.10.dat'))
    files_are_same(os.path.join(react_dir, 'a.dat'), os.path.join(dir, react_dir, 'a.dat'), 5)
    
    