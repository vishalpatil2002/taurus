# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/usr/include/eigen3".split(';') if "${prefix}/include;/usr/include/eigen3" != "" else []
PROJECT_CATKIN_DEPENDS = "tf2_ros;costmap_2d;roscpp;roslib;geometry_msgs;move_base_msgs;actionlib;message_filters;base_local_planner;angles;pluginlib;sensor_msgs;filters".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-llaser_scan_max_range_filter".split(';') if "-llaser_scan_max_range_filter" != "" else []
PROJECT_NAME = "assisted_teleop"
PROJECT_SPACE_DIR = "/home/vijay/taurus/big_taurus/install"
PROJECT_VERSION = "0.3.6"
