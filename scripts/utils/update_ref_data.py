import os
import sys
import shutil

#SEED_DIR = 'seed_00001'
SEED_DIR = 'seed_56362'

def update_dir(work_data_dir, test_data_dir):
    files = os.listdir(test_data_dir)
    for fname in files:
        print("  - updating " + fname)
        shutil.copy(os.path.join(work_data_dir, fname), os.path.join(test_data_dir, fname))

def update_ref_data(work_dir, test_dir):
    print("Updating MCell4 ref data in " + test_dir + " using data from " + work_dir)

    work_viz_seed = os.path.join(work_dir, 'viz_data', SEED_DIR);
    test_viz_seed = os.path.join(test_dir, 'ref_viz_data_4', SEED_DIR);

    work_react_seed = os.path.join(work_dir, 'react_data', SEED_DIR);
    test_react_seed = os.path.join(test_dir, 'ref_react_data_4', SEED_DIR);
    
    update_dir(work_viz_seed, test_viz_seed)
    
    if (os.path.exists(test_react_seed)):
        update_dir(work_react_seed, test_react_seed)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Expecting work directory and test directory")
        sys.exit(1)
    
    update_ref_data(sys.argv[1], sys.argv[2])
