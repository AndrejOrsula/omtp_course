cmake_minimum_required(VERSION 2.8.3)
project(omtp_modified)

find_package(
  catkin REQUIRED COMPONENTS joint_state_publisher robot_state_publisher rviz
                             ur_description xacro)

catkin_package(
  # INCLUDE_DIRS include LIBRARIES omtp_support CATKIN_DEPENDS
  # joint_state_publisher robot_state_publisher rviz ur_description xacro
  # DEPENDS system_lib
)

include_directories(# include
                    ${catkin_INCLUDE_DIRS})

install(DIRECTORY launch urdf DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
