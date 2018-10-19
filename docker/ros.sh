#!/bin/bash

echo "ARGUMENTS: $@"
cd /code/ws/mesh
source install/setup.bash -
#vglrun rosrun --prefix "gdb -ex run --args" symmetry_annotate find_reflection "$@"
#vglrun rosrun symmetry_annotate find_reflection "$@"
