# Setup
First, install Docker.

Next, run `docker pull convolve/crp-mod-2`. This is the Docker container you will need.
It is about 2 GB.

Finally, clone this repo. Once you have done this, you will need to use `chmod +x` to make 
`call_crp.py`, `run_script.sh`, and `simulate.sh` executable.

# Usage
The Python script that runs simulations is MC_full3a.py. In order to run it with n iterations,
run `./simulate.sh n`. This will use `6T5_data_to_simulate.txt` as the input events, and output the iterations on each 
event to the `samples/` folder.

# Notes
One thing to note is that you will not have write permission on the output files. This is a consequence of using Docker.
In order to move or delete the output files, you'll have to use `chown` to give yourself ownership.