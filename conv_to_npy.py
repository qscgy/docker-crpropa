import numpy as np


filename = 'samples/evt_1_a.txt'
data = np.loadtxt(filename, dtype=np.float64)
np.save('samples/evt_1_a.npy', data)

data_np = np.load('samples/evt_1_a.npy')
print(data_np.shape)
