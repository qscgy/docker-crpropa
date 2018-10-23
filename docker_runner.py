import os
from os.path import abspath, join
import sys
import subprocess

workdir = os.getcwd()   # current working directory
prog = abspath(join(workdir, str(sys.argv[1])))  # absolute path to the script we want to run
print(workdir)

# use the docker container "convolve/crpropa" to run our script, then make the output file editable to the host
completed = subprocess.run(['docker', 'run', '-it', '-v', workdir+str(':/cosmicrays'), 'convolve/crpropa', 'bash',
                            '-c', "python cosmicrays/"+str(sys.argv[1])+" && chmod 777 cosmicrays/plot.png"+
                            " && chmod 777 cosmicrays/galactic_trajectories.txt"])
print('returncode: ', completed.returncode)
