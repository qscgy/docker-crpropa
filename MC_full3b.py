import numpy as np
import scipy.stats as ss
import random
import subprocess as sp


def running_in_docker():
    with open('/proc/self/cgroup', 'r') as procfile:
        for line in procfile:
            fields = line.strip().split('/')
            if 'docker' in fields:
                return True

    return False


docker = running_in_docker()
print(docker)
infile = "6T5_data_to_simulate.txt"
call_crp = "call_crp.py"
if docker:
    infile = "cosmicrays/"+infile
    call_crp = "cosmicrays/"+call_crp
else:
    call_crp = "./"+call_crp


evt_id = np.loadtxt(infile, usecols=(3,), dtype=np.float64)
E, glon, glat = np.loadtxt(infile, usecols=(0, 1, 2), unpack=True)  # TODO cols should be 5, 1, 2

for i in range(1):

    ID = evt_id[i]

    outfile = 'samples/evt_%i_b.txt' % ID
    if docker:
        outfile = "cosmicrays/" + outfile

    data_array = np.zeros((100, 9))     # TODO change to (20000, 9)

    for j in range(100):    # TODO change to (20000, 40000)
        print("Iteration %i / %i" % (j, 100))
        if j % 50 == 0:
            np.savetxt(outfile % ID, data_array)  # Save to disk every 1000 iterations
        s1, s2, s3 = random.sample(range(1, 2 ** 26 - 1), 3)
        cmd = ['timeout', '35', call_crp, '%f' % E[i],
               '%f' % glon[i], '%f' % glat[i], '%i' % s1, '%i' % s2, '%i' % s3]
        proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)
        out, err = proc.communicate()
        out = out.decode('ascii')
        try:
            # out = out.replace('(', '')
            # out = out.replace(')', '')
            out = out.replace('\n', '')
            out = out.split(' ')
            out = [float(m) for m in out]
            # for k in range(8):
            #     data_array[j - 20000, k] = out[k]
            for k in range(8):
                data_array[j, k] = out[k]
        except:
            # data_array[j - 20000, 8] = 1.
            data_array[j, 8] = 1.
            print("Timeout")
        print(out)
    np.savetxt(outfile % ID, data_array)
