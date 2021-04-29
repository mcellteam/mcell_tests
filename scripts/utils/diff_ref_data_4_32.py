import os
import sys
import shutil

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(THIS_DIR, '..'))
import data_output_diff


def diff_ref_data_4_32(test_dir, test_name):
    print("Comparing MCell4 ref data in " + test_name + ".")

    test_viz_seed = os.path.join(test_dir, test_name, 'ref_viz_data_4', 'seed_00001');
    test_viz_seed_32 = os.path.join(test_dir, test_name, 'ref_viz_data_4_32', 'seed_00001');

    test_react_seed = os.path.join(test_dir, test_name, 'ref_react_data_4', 'seed_00001');
    test_react_seed_32 = os.path.join(test_dir, test_name, 'ref_react_data_4_32', 'seed_00001');

    res = data_output_diff.compare_data_output_directory(test_viz_seed, test_viz_seed_32, False, ['1e-6'])
    if res != data_output_diff.PASSED:
        print("Test " + test_name + "failed")
    
    
if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Expecting test names")
        sys.exit(1)
    
    for test_name in sys.argv[1:]:
        diff_ref_data_4_32(os.getcwd(), test_name)
