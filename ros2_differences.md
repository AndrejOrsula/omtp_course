# *ROS 2* Differences
![OS](https://img.shields.io/badge/OS-Ubuntu_18.04-orange.svg) ![ROS_2](https://img.shields.io/badge/ROS_2-Eloquent-brightgreen.svg)

This document provides description of the main differences between *ROS 1* and *ROS 2* that were encountered during the OMTP course by group ROB866. Furthermore, it details some of the difficulties encountered during the process, together with the found solution, workaround or a description of the possible cause.


## Porting of URDF to *ROS 2*
The *ROS 1* packages obviously need to be ported to *ROS 2* before their utilisation. The simplies approach seems to be
```bash
ros2 pkg create <ros2_pkg_name>
cp -r /path/to/<ros1_pkg_name>/urdf /path/to/<ros2_pkg_name>/urdf
cp -r /path/to/<ros1_pkg_name>/meshes /path/to/<ros2_pkg_name>/meshes
```
and including both directories in the `CMake` installation.

However, the URDF description files do not seem to work out of the box. The problem was attributed to the local package path specifiers in `.xacro` files, "package://<ros1_pkg_name>", which prevents loading of the visual and collision models (no warning/error messages are logged, so it is a bit tough to find the problem). Solution is to replace local package specifiers with "$(find <ros2_pkg_name>)" substitution.
```bash
sed -i 's|package://<ros1_pkg_name>|$(find <ros2_pkg_name>)|g' /path/to/<ros2_pkg_name>/urdf/*
```


### Duplicate Joint of **omtp_factory**
The **omtp_factory** contains a duplicate joint between `world_interface` and `robot1_pedestal_link`, which causes the UR to have an unexpected placement in the world (as if the transformation was applied twice).

Therefore, the following joint had to be removed from `omtp_factory.xacro`:
```xml
<!-- robot1-pedestal to world. -->
<joint name="robot1_pedestal_to_world_interface" type="fixed">
    <parent link="world_interface" />
    <child link="robot1_pedestal_link" />
    <origin xyz="0.5 1.8 0.0" rpy="0.0 0.0 0.0"/>
</joint>
```


### Unknown issue with **abb_irb6640**
We were not able to make [**abb_irb6640**](https://github.com/ros-industrial/abb/tree/kinetic-devel/abb_irb6640_support) load properly in *Gazebo*. The kinematic chain seems to be correct, however, only the model of the base would be loaded into *Gazebo*. The cause of this issue is unclear, but likely caused by something small in the joint description that is not compatible with *ROS 2*.
