#!/usr/bin/env bash

BASE_CODE=$HOME/dev
DATA_DIR=/home/data/jlowens

DOCKER_IP=$(ifconfig docker0 | grep 'inet addr' | sed -re's/.*inet addr:([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*/\1/')

CMD=${@:-"/bin/bash"}
#xhost +$DOCKER_IP
xhost +
nvidia-docker run --rm -it \
	      --net=host \
	      -v $BASE_CODE:/code \
	      -v $DATA_DIR:$DATA_DIR \
	      -v $HOME/.Xauthority:/home/user/.Xauthority:rw \
	      -v /etc/opt/VirtualGL:/etc/opt/VirtualGL \
	      -e LOCAL_USER_ID=$(id -u) \
	      -e LOCAL_GROUP_ID=$(id -g) \
	      -e DISPLAY=$DISPLAY \
	      -e VGL_CLIENT=$VGL_CLIENT \
	      -e VGL_DISPLAY=:0.0 \
	      --privileged \
	      -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
	      jlowenz/keras-with-ros:2.0 $CMD
xhost -
