import os
from os.path import abspath, join
import sys
import subprocess

workdir = os.getcwd()
prog = abspath(join(workdir, str(sys.argv[1])))
print(workdir)

completed = subprocess.run(['docker', 'run', '-it', '-v', workdir+str(':/cosmicrays'), 'convolve/crpropa', 'bash',
                            '-c', "python cosmicrays/"+str(sys.argv[1])+" && chmod 777 cosmicrays/plot.png"])
print('returncode: ', completed.returncode)
