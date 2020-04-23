cmake_minimum_required(VERSION 2.8.3)
project(omtp_support)

add_definitions(-std=c++11)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY config meshes launch urdf
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
