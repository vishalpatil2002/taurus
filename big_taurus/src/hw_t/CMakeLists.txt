cmake_minimum_required(VERSION 3.0.2)
project(hw_t)

## Compile as C++11
add_compile_options(-std=c++11)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  angles
  controller_manager
  geometry_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  actionlib_msgs
  actionlib
  message_generation
)

add_action_files(
  FILES
  Lift.action
  Conveyor.action
  aruco_detect.action
 
 machineControl.action
)

add_message_files(
  FILES
  bms.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs  actionlib_msgs
)
## Find libmodbus
find_package(PkgConfig REQUIRED)
pkg_check_modules(MODBUS REQUIRED libmodbus)

###################################
## catkin specific configuration ##
###################################
catkin_package(
  INCLUDE_DIRS include
  LIBRARIES hw_t moonsModbus
  CATKIN_DEPENDS angles actionlib actionlib_msgs controller_manager roscpp rospy sensor_msgs std_msgs message_runtime
)

catkin_install_python(PROGRAMS
  scripts/network_check.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
catkin_install_python(PROGRAMS scripts/teleop.py  scripts/machineControlClient.py scripts/machineControlSever.py scripts/new_dockin.py scripts/machineControlClient_plc.py scripts/machineControlServer.py scripts/test_server.py scripts/test_stn41.py scripts/loadAndunloadClient.py scripts/loadAndunloadServer.py
scripts/loadunloadServer2.py

DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


###########
## Build ##
###########

## Specify include directories
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${MODBUS_INCLUDE_DIRS}
)

## Build moonsModbus library
add_library(moonsModbus
  src/moonsModbus.cpp
)
target_link_libraries(moonsModbus ${catkin_LIBRARIES} ${MODBUS_LIBRARIES})
add_dependencies(moonsModbus ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Build Taurus node executable
add_executable(taurus_node
  src/taurus_node.cpp
)
target_link_libraries(taurus_node moonsModbus ${catkin_LIBRARIES} ${MODBUS_LIBRARIES})
add_dependencies(taurus_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

add_executable(lift_action src/lift_action.cpp src/lift_function.cpp)
target_link_libraries(lift_action ${catkin_LIBRARIES} ${MODBUS_LIBRARIES})

add_executable(lift_client src/lift_client.cpp)
target_link_libraries(lift_client ${catkin_LIBRARIES})

add_dependencies(lift_action hw_t_generate_messages_cpp)
add_dependencies(lift_client hw_t_generate_messages_cpp)

add_executable(conveyor_action src/conveyor_action.cpp src/conveyor_function.cpp)
target_link_libraries(conveyor_action ${catkin_LIBRARIES} ${MODBUS_LIBRARIES})

add_executable(conveyor_client src/conveyor_client.cpp)
target_link_libraries(conveyor_client ${catkin_LIBRARIES})

add_dependencies(conveyor_action hw_t_generate_messages_cpp)
add_dependencies(conveyor_client hw_t_generate_messages_cpp)

add_executable(taurus_test
  src/test_motor.cpp
)

target_link_libraries(taurus_test
  moonsModbus
  ${catkin_LIBRARIES}
)

add_dependencies(taurus_test
  ${${PROJECT_NAME}_EXPORTED_TARGETS}
  ${catkin_EXPORTED_TARGETS}
)

#############
## Install ##
#############
## Install executable
install(TARGETS taurus_node
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Install libraries
install(TARGETS moonsModbus
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Install header files
install(DIRECTORY include/hw_t/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
)

## Install launch files
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)


## Install config files
install(DIRECTORY config/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
)

## Install URDF/xacro files
install(DIRECTORY urdf/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/urdf
)

