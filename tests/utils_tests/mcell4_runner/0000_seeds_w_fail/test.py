import sys

# expected to be run as mcell4_runner.py test1.py -s 1:3:1

assert len(sys.argv) == 3
assert sys.argv[1] == '-seed'

seed = int(sys.argv[2])
if seed == 3:
    sys.stderr.write('expected fail\n')
    sys.exit(1)
elif seed >= 1 and seed <= 2:
    print('ok')
else:
    assert False
        