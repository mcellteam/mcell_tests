import math
# sin * 1000 + 5000

for i in range(10000):
    print("{:.6f}".format(i*1e-5) + "    " + "{:.2f}".format(((i/10000 * (math.sin(i/100)+1)*300)) * 1e5))