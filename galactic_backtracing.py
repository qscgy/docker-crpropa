from crpropa import *
import matplotlib.pyplot as plt
import numpy as np

B = JF12Field()
# seed = 691342
# B.randomStriated(seed)
# B.randomTurbulent(seed)

sim = ModuleList()
sim.add(PropagationCK(B, 1e-4, 0.1*parsec, 100*parsec))
obs = Observer()
obs.add(ObserverLargeSphere(Vector3d(0), 20*kpc))
# obs.onDetection(TextOutput('galactic_backtracking.txt', Output.Event3D))
sim.add(obs)
print(sim)

R = Random()

pid = -nucleusId(1, 1)  # antiproton
meanEnergy = 10*EeV
sigmaEnergy = 0.1*meanEnergy
lat0 = 1.96
lon0 = 1.95
position = Vector3d(-8.5, 0, 0)*kpc
meanDir = Vector3d()
meanDir.setRThetaPhi(1, lat0, lon0)
sigmaDir = 0.002

lons, lats = [], []
for i in range(100):
    energy = R.randNorm(meanEnergy, sigmaEnergy)
    direction = R.randVectorAroundMean(meanDir, sigmaDir)
    p = ParticleState(pid, energy, position, direction)
    c = Candidate(p)
    sim.run(c)
    d1 = c.current.getDirection()
    lons.append(d1.getPhi())
    lats.append(d1.getTheta())
    print(direction.getAngleTo(d1))

lat0 = np.pi/2 - lat0
lats = np.pi/2 - np.array(lats)

plt.figure(figsize=(12, 7))
plt.subplot(111, projection='hammer')
plt.scatter(lon0, lat0, marker='+', c='black', s=100)
plt.scatter(lons, lats, marker='o', c='blue', linewidths=0, alpha=0.2)
plt.grid(True)
plt.show()

