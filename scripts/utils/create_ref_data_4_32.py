import os
import sys
import shutil


def copy_test_dir(work_data_dir, test_data_dir, test_data_dir_32):
    files = os.listdir(test_data_dir)
    
    if not os.path.exists(test_data_dir_32):
        os.makedirs(test_data_dir_32)
    
    for fname in files:
        print("  - updating " + fname)
        shutil.copy(os.path.join(work_data_dir, fname), os.path.join(test_data_dir_32, fname))

def create_ref_data_4_32(work_dir, test_dir, test_name):
    print("Updating MCell4 ref data in " + test_dir + " using data from " + work_dir)

    work_viz_seed = os.path.join(work_dir, test_name, 'viz_data', 'seed_00001');
    test_viz_seed = os.path.join(test_dir, test_name, 'ref_viz_data_4', 'seed_00001');
    test_viz_seed_32 = os.path.join(test_dir, test_name, 'ref_viz_data_4_32', 'seed_00001');

    work_react_seed = os.path.join(work_dir, test_name, 'react_data', 'seed_00001');
    test_react_seed = os.path.join(test_dir, test_name, 'ref_react_data_4', 'seed_00001');
    test_react_seed_32 = os.path.join(test_dir, test_name, 'ref_react_data_4_32', 'seed_00001');
    
    copy_test_dir(work_viz_seed, test_viz_seed, test_viz_seed_32)
    
    if (os.path.exists(test_react_seed)):
        copy_test_dir(work_react_seed, test_react_seed, test_react_seed_32)
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Expecting work directory and test directory and test names")
        sys.exit(1)
    
    for test_name in sys.argv[3:]:
        create_ref_data_4_32(sys.argv[1], sys.argv[2], test_name)
