import numpy as np
import scipy.stats as ss
import random
import subprocess as sp
import sys
import cchardet

evt_id = np.loadtxt("6T5_data_to_simulate.txt", usecols=(0,), dtype=np.float64)
E, glon, glat = np.loadtxt("6T5_data_to_simulate.txt", usecols=(0, 1, 2), unpack=True)  # TODO cols should be 5, 1, 2

for i in range(1):  # TODO change back to 10
    ID = evt_id[i]

    data_array = np.zeros((5, 9))     # TODO change 5 back to 20000

    for j in range(5):
        if j % 50 == 0:
            # np.savetxt('samples/evt_%i_a.txt' % ID, data_array)  # Save to disk every 1000 iterations
            print("Iteration %i / %i" % (j, 5))
        s1, s2, s3 = random.sample(range(1, 2 ** 26 - 1), 3)
        # print('{0} {1} {2}'.format(s1, s2, s3))
        cmd = ['timeout', '35', './call_crp.py', '%f' % E[i],
               '%f' % glon[i], '%f' % glat[i], '%i' % s1, '%i' % s2, '%i' % s3]
        proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)
        out, err = proc.communicate()
        out = out.decode('ascii')

        # out = out.decode('utf-8')
        # out = sp.check_output(cmd)
        # out = str(out, 'utf-8')
        try:
            # out = out.replace('(', '')
            # out = out.replace(')', '')
            out = out.replace('\n', '')
            out = out.split(' ')
            out = [float(m) for m in out]
            for k in range(8):
                data_array[j, k] = out[k]
        except:
            data_array[j, 8] = 1.
            print("Timeout")
        print(out)
        print(type(data_array[j, 0]))
    np.savetxt('samples/evt_%i_a.txt' % ID, data_array)
