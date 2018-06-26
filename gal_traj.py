from crpropa import *
import sys, os
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import shutil


def runningInDocker():
    with open('/proc/self/cgroup', 'r') as procfile:
        for line in procfile:
            fields = line.strip().split('/')
            if 'docker' in fields:
                return True

    return False


B = JF12Field()
randomSeed = 691432
B.randomStriated(randomSeed)
B.randomTurbulent(randomSeed)

sim = ModuleList()
sim.add(PropagationCK(B, 1e-4, 0.1*parsec, 100*parsec))
sim.add(SphericalBoundary(Vector3d(0), 20*kpc))


class MyTrajectoryOutput(Module):
    def __init__(self, fname):
        Module.__init__(self)
        self.fout = open(fname, 'w')
        self.i = 0

    def process(self, c):
        v = c.current.getPosition()
        x = v.x/kpc
        y = v.y/kpc
        z = v.z/kpc
        self.fout.write('%i\t%.3f\t%.3f\t%.3f\n' % (self.i, x, y, z))
        if not(c.isActive()):
            self.i += 1

    def close(self):
        self.fout.close()


output = MyTrajectoryOutput('galactic_trajectories.txt')
sim.add(output)

# source = Source()
# source.add(SourcePosition(Vector3d(-8.5, 0, 0)*kpc))
# source.add(SourceIsotropicEmission())
# source.add(SourceParticleType(-nucleusId(1, 1)))
# source.add(SourceEnergy(10*EeV))

# sim.run(source, 10)

# In order to backtrace a particle, we do a forward trace of its antiparticle. We say that it starts at the earth and
# is initially travelling in its observed arrival direction. We then simply simulate the particle until it reaches our
# simulation boundary.
pid = -nucleusId(4, 2)
energy = 1*EeV
position = Vector3d(-8.5, 0, 0)*kpc     # position of the Earth in the galaxy
direction = Vector3d()
direction.setRThetaPhi(1, -1.96, 1.95)  # the arrival direction (in galactocentric coordinates)
particle = ParticleState(pid, energy, position, direction)
candidate = Candidate(particle)
sim.run(candidate)

output.close()

if runningInDocker():
    # print(runningInDocker())
    import matplotlib
    matplotlib.use('agg')

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 12))
ax = plt.subplot(111, projection='3d', aspect='equal')

I, X, Y, Z = np.genfromtxt('galactic_trajectories.txt', unpack=True, skip_footer=1)
for i in range(int(max(I)+1)):
    # print(X)
    idx = I == i
    ax.plot(X[idx], Y[idx], Z[idx], c='b', lw=1, alpha=0.5)

r = 20
u, v = np.meshgrid(np.linspace(0, 2*np.pi, 100), np.linspace(0, np.pi, 100))
x = r*np.cos(u)*np.sin(v)
y = r*np.sin(u)*np.sin(v)
z = r*np.cos(v)
ax.plot_surface(x, y, z, rstride=2, cstride=2, color='r', alpha=0.1, lw=0)
ax.plot_wireframe(x, y, z, rstride=10, cstride=10, color='k', alpha=0.5, lw=0.3)

ax.scatter(0, 0, 0, marker='o', color='k')
ax.scatter(-8.5, 0, 0, color='b', marker='o')

ax.tick_params(axis='both', which='major', labelsize=16)
ax.tick_params(axis='both', which='minor', labelsize=16)
ax.set_xlabel('x (kpc)', fontsize=18)
ax.set_ylabel('y (kpc)', fontsize=18)
ax.set_zlabel('z (kpc)', fontsize=18)
ax.set_xlim((-20, 20))
ax.set_ylim((-20, 20))
ax.set_zlim((-20, 20))
ax.xaxis.set_ticks((-20,-10,0,10,20))
ax.yaxis.set_ticks((-20,-10,0,10,20))
ax.zaxis.set_ticks((-20,-10,0,10,20))

if runningInDocker():
    print("Running in Docker")
    plt.savefig('/cosmicrays/plot.png', format='png')
    if os.path.isfile('/cosmicrays/plot.png'):
        print('Plot created')
    # os.system("ls /cosmicrays")
else:
    plt.show()
