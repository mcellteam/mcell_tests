import sys

# expected to be run as mcell4_runner.py test2.py -a test2_args.txt

assert len(sys.argv) == 4
assert sys.argv[1] == '-seed'

seed = int(sys.argv[2])
if seed == 1:
    assert sys.argv[3] == 'A'
elif seed == 2:
    assert sys.argv[3] == 'B'
elif seed == 3:
    assert sys.argv[3] == 'C'
else:
    assert False
        