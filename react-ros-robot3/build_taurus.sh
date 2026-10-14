#!/bin/bash
set -e

source /opt/ros/noetic/setup.bash

cd "$(dirname "$0")/big_taurus"

rm -rf build devel
catkin_make
source devel/setup.bash

echo "Taurus workspace built successfully"
