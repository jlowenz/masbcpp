#!/bin/bash

cd /code/ws/mesh
source install/setup.bash
exec rosrun mesh2pcd mesh2pcd $@
