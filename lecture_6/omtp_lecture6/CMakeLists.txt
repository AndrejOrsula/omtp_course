cmake_minimum_required(VERSION 2.8.3)
project(omtp_lecture6)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY config launch scripts
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
