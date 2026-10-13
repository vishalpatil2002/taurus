# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/opt/ros/noetic/include".split(';') if "${prefix}/include;/opt/ros/noetic/include" != "" else []
PROJECT_CATKIN_DEPENDS = "roscpp;costmap_2d;nav_core;pluginlib;tf;tf2;geometry_msgs;nav_msgs;message_runtime".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lsbpl_lattice_planner;/opt/ros/noetic/lib/libsbpl.so".split(';') if "-lsbpl_lattice_planner;/opt/ros/noetic/lib/libsbpl.so" != "" else []
PROJECT_NAME = "sbpl_lattice_planner"
PROJECT_SPACE_DIR = "/home/vijay/taurus/big_taurus/install"
PROJECT_VERSION = "0.3.6"
