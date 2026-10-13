# Install script for directory: /home/vijay/taurus/big_taurus/src/hw_t

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/vijay/taurus/big_taurus/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/action" TYPE FILE FILES
    "/home/vijay/taurus/big_taurus/src/hw_t/action/Lift.action"
    "/home/vijay/taurus/big_taurus/src/hw_t/action/Conveyor.action"
    "/home/vijay/taurus/big_taurus/src/hw_t/action/aruco_detect.action"
    "/home/vijay/taurus/big_taurus/src/hw_t/action/machineControl.action"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/msg" TYPE FILE FILES
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/LiftAction.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/LiftActionGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/LiftActionResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/LiftActionFeedback.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/LiftGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/LiftResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/LiftFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/msg" TYPE FILE FILES
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/ConveyorAction.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/ConveyorActionGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/ConveyorActionResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/ConveyorActionFeedback.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/ConveyorGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/ConveyorResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/ConveyorFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/msg" TYPE FILE FILES
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/aruco_detectAction.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/aruco_detectActionGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/aruco_detectActionResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/aruco_detectActionFeedback.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/aruco_detectGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/aruco_detectResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/aruco_detectFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/msg" TYPE FILE FILES
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/machineControlAction.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/machineControlActionGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/machineControlActionResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/machineControlActionFeedback.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/machineControlGoal.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/machineControlResult.msg"
    "/home/vijay/taurus/big_taurus/devel/share/hw_t/msg/machineControlFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/msg" TYPE FILE FILES "/home/vijay/taurus/big_taurus/src/hw_t/msg/bms.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/cmake" TYPE FILE FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/hw_t-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/devel/include/hw_t")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/devel/share/roseus/ros/hw_t")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/devel/share/common-lisp/ros/hw_t")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/devel/share/gennodejs/ros/hw_t")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/vijay/taurus/big_taurus/devel/lib/python3/dist-packages/hw_t")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/devel/lib/python3/dist-packages/hw_t")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/hw_t.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/cmake" TYPE FILE FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/hw_t-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/cmake" TYPE FILE FILES
    "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/hw_tConfig.cmake"
    "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/hw_tConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t" TYPE FILE FILES "/home/vijay/taurus/big_taurus/src/hw_t/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/network_check.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/teleop.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/machineControlClient.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/machineControlSever.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/new_dockin.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/machineControlClient_plc.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/machineControlServer.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/test_server.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/test_stn41.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/loadAndunloadClient.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/loadAndunloadServer.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE PROGRAM FILES "/home/vijay/taurus/big_taurus/build/hw_t/catkin_generated/installspace/loadunloadServer2.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/hw_t/taurus_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/hw_t/taurus_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/hw_t/taurus_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hw_t" TYPE EXECUTABLE FILES "/home/vijay/taurus/big_taurus/devel/lib/hw_t/taurus_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/hw_t/taurus_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/hw_t/taurus_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/hw_t/taurus_node"
         OLD_RPATH "/home/vijay/taurus/big_taurus/devel/lib:/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/hw_t/taurus_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoonsModbus.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoonsModbus.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoonsModbus.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/vijay/taurus/big_taurus/devel/lib/libmoonsModbus.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoonsModbus.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoonsModbus.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoonsModbus.so"
         OLD_RPATH "/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoonsModbus.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/hw_t" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/src/hw_t/include/hw_t/" FILES_MATCHING REGEX "/[^/]*\\.h$" REGEX "/[^/]*\\.hpp$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/launch" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/src/hw_t/launch/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/config" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/src/hw_t/config/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hw_t/urdf" TYPE DIRECTORY FILES "/home/vijay/taurus/big_taurus/src/hw_t/urdf/")
endif()

