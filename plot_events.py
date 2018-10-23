import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from crpropa import *
from numpy.random import random


# Make maps and stuff of Auger data.


# AugerId
# Number of Selected Stations
# Local Theta
# Local Phi
# Energy
# L
# B
# UTC Time
# TCore
# XCore
# YCore
# S1000
# dS1000
# Ra
# Dec
# Theta (should not be used)
# Phi (should not be used)
# dTheta
# dPhi
# dXCore
# dYCore
# Etimation and Reconstruction compatibles
# Is T5
# Is T5+
# Is T5++
# Is ICRC2005
# Is Fd trigger
# Geometric fit Chi2
# LDF fit Chi2
# Global fit Chi2
# Global fit Ndof
# LDF Beta
# LDF Gamma
# R
# OldId
# IsICRC2005Posterior
# Icrc Energy
# Delta Omega
# Delta Core


def get_useful_info(event):
    print("Multiplicity: {0} Energy: {1} Flag 22: {2} Flag 23: {3}".format(event[1], event[4], event[21], event[22]))
    print(event)


def process_raw_auger(fname, sep, skiprows):
    df = pd.read_table(fname, sep=sep, skiprows=skiprows)
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
    mask = np.ma.array(largest, mask=False)
    # print(mask)
    for i in range(largest.shape[0]):
        # filter out events that didn't reconstruct
        if int(data_t[1, largest[i]]) == -1 or data_t[21, largest[i]] == 0.0:
            mask[i] = np.ma.masked
        elif energies[i] > 10000:
            get_useful_info(data[largest[i]])
            # mask[i] = np.ma.masked
    largest = mask.compressed()
    # print(largest)
    energies = data_t[4, largest]
    # print(energies)
    # print(np.count_nonzero(energies == 0.192373))
    l = data_t[5, largest]
    b = data_t[6, largest]
    # plt.hist(energies, bins=200)
    # plt.show()
    return energies, l, b


def process_sim_output(fname):
    data = np.genfromtxt(fname, dtype=np.float64)
    energies = data[:, 0]
    pos = data[:, 1:4]
    print(pos.shape)
    ls = np.zeros(data.shape[0])
    bs = np.zeros(data.shape[0])
    for i in range(data.shape[0]):
        x, y, z = pos[i]
        vec = Vector3d(x, y, z)
        ls[i] = vec.getPhi()*180.0/np.pi
        bs[i] = vec.getTheta()*180.0/np.pi
    return energies, ls, bs

def generate_fake_data(n):
    i = 0
    energies = np.zeros(n)
    gal_l = np.zeros(n)
    gal_b = np.zeros(n)
    for i in range(n):
        energies[i] = np.power(10, 21-np.log10(1000-999*random())-18)
        gal_l[i] = random()*360.0-180.0
        gal_b[i] = random()*180.0-90.0
        i += 1
    return energies, gal_l, gal_b


# energies, l, b = process_raw_auger('/home/sam/Downloads/auger-data/Archive', '\s+', 7)
energies, l, b = process_sim_output('samples/evt_0_a.txt')
# energies2, l2, b2 = generate_fake_data(1000)

fig = plt.figure(figsize=(12, 9), edgecolor='w')
plt.subplot('211')
# plt.hist(energies2, bins=40)
m = Basemap(projection='hammer', lon_0=-80)
# print(energies)
# lat, lon = 29.7630556,-95.3630556
# x, y = m(lon, lat)
x, y = m(l, b)
m.scatter(x, y, c=energies, cmap='plasma')
m.colorbar()

plt.subplot('212')
plt.hist(energies, bins=40)
# hist, bins = np.histogram(energies, bins=20)
# plt.loglog(bins[1:], hist, marker='o', linestyle='None')
plt.show()
