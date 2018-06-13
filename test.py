from crpropa import *
import matplotlib.pyplot as plt
import numpy as np

sim = ModuleList()

sim.add(SimplePropagation())

sim.add(PhotoPionProduction(CMB))
sim.add(ElectronPairProduction(CMB))
sim.add(NuclearDecay())
sim.add(MinimumEnergy(1*EeV))

# cosmicray = Candidate(nucleusId(1, 1), 200*EeV, Vector3d(100*Mpc, 0, 0))
#
# sim.run(cosmicray)
#
# print(cosmicray)
# print('Propagated distance:', cosmicray.getTrajectoryLength()/Mpc, " Mpc")

obs = Observer()
obs.add(ObserverPoint())
sim.add(obs)
print(obs)

output1 = TextOutput('trajectories.txt', Output.Trajectory1D)
sim.add(output1)
output1.disableAll()
# output1.enable(Output.CurrentEnergyColumn)

output2 = TextOutput('events.txt', Output.Event1D)
obs.onDetection(output2)    # Only call the observer on detection

source = Source()
source.add(SourcePosition(100*Mpc))
source.add(SourceParticleType(nucleusId(1, 1)))
source.add(SourcePowerLawSpectrum(1*EeV, 200*EeV, -1))
print(source)

sim.setShowProgress(True)
sim.run(source, 10000)

output2.close()
data = np.genfromtxt('events.txt', names=True)
print('Number of events: ', len(data))

logE0 = np.log10(data['E0']) + 18
logE = np.log10(data['E']) + 18

plt.figure(figsize=(10, 7))
h1 = plt.hist(logE0, bins=25, range=(18, 20.5), histtype='stepfilled', alpha=0.5, label='At source')
h2 = plt.hist(logE, bins=25, range=(18, 20.5), histtype='stepfilled', alpha=0.5, label='Observed')
plt.show()
