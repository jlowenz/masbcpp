#!/bin/bash

cd /code/ws/mesh
source install/setup.bash
cd src/annotate_symmetry/notebooks
echo "import numpy as np; import rospy; rospy.init_node('blah',anonymous=True)" > ~/.pyrc
export PYTHONSTARTUP=~/.pyrc
#vglrun gdb --args python /usr/local/bin/ipython
CUDA_VISIBLE_DEVICES=$1 ipython notebook
