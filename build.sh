#!/bin/sh
rosdep install --from-path src/ -y -i
catkin_make
source ./devel/setup.sh
