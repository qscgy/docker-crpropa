import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fname = '/home/sam/Documents/test_crt.out'
data = np.genfromtxt(fname, comments='#', unpack=True, skip_footer=1)

plt.figure(figsize=(12, 12))
ax = plt.subplot(111, projection='3d')
index, x, y, z = data[0:4]
for i in range(int(max(index)+1)):
    filter = index==i
    ax.plot(x[filter], y[filter], z[filter], lw=1, alpha=0.5)

plt.show()
