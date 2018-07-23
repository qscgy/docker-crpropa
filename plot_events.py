import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

df = pd.read_table('/home/sam/Downloads/auger-data/Archive', sep='\s+', skiprows=7)
df.fillna(0.0, inplace=True)

data = df.values
data_t = df.values.transpose()
# print(data_t.shape)

nmost = 2000
largest = np.argpartition(data_t[4], -nmost)[-nmost:]

# print(largest)
# plt.figure()
energies = data_t[4, largest]
# h = np.histogram(energies, bins=20)
largest = np.ma.array(largest, mask=False)
for i in range(largest.shape[0]):
    # filter out abnormally large values or values where missing values had to be filled in with 0
    if energies[i] > 200 or abs(data_t[38, largest[i]]) < 0.000001:
        largest[i] = True
energies = data_t[4, largest]
l = data_t[5, largest]
b = data_t[6, largest]
for i in largest:
    if abs(data_t[5, i]) < 1:
        print(data[i])
# plt.hist(energies, bins=200)
# plt.show()


fig = plt.figure(figsize=(12, 9), edgecolor='w')
m = Basemap(projection='hammer', lon_0=-80)
# m.drawcoastlines()

# lat, lon = 29.7630556,-95.3630556
# x, y = m(lon, lat)
x, y = m(l, b)
m.scatter(x, y, c=energies, cmap='plasma')
m.colorbar()
plt.show()
