#!/bin/bash

xhost +local:docker
export DISPLAY=$DISPLAY
export XAUTH=/tmp/.docker.xauth
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

cd ~/robot_system
docker-compose -f docker/docker-compose.yml up -d
