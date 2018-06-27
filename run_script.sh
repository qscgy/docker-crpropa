#!/usr/bin/env bash

workdir=`pwd`
prog="$workdir/$1"
containerprog="cosmicrays/$1"

# && chmod 777 cosmicrays/plot.png && chmod 777 cosmicrays/galactic_trajectories.txt
docker run -it -v "$workdir:/cosmicrays" convolve/crpropa "$1"