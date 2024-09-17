#!/bin/bash

xhost +local:docker
sudo docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix automated_planogram