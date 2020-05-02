# ROB866 - OMTP
![OS](https://img.shields.io/badge/OS-Ubuntu_18.04-orange.svg) ![ROS_1](https://img.shields.io/badge/ROS_1-Melodic-blue.svg) ![GAZEBO](https://img.shields.io/badge/Gazebo-9.12-lightgrey.svg)

This repository contains assignment of group ROB866 for *Object Manipulation and Task Planning (Robotics 8)* course at *Aalborg University*, *Denmark*.


## Assignments
- [lecture 1](lecture_1/) - URDF and XACRO
- [lecture 5](lecture_5/) - MoveIt Basics
- [lecture 6](lecture_6/) - Object Detection and Grasping


## Installation
The following installation instructions were tested with OS based on *Ubuntu 18.04 LTS (Bionic Beaver)*.

### Requirements
Please install the following either as Debian packages or build them from source.
- [ROS 1 Melodic](http://wiki.ros.org/melodic/Installation/Ubuntu)
- [colcon](https://colcon.readthedocs.io/en/released/user/installation.html) or [catkin_tools](https://catkin-tools.readthedocs.io/en/latest/installing.html)

### Building
If not a part of `~/.bashrc`, make sure to source the global ROS installation.
```bash
source /opt/ros/melodic/setup.bash
```

Hereafter, you can clone this repository
```bash
mkdir -p awesome_ws/src && cd awesome_ws
git clone https://github.com/AndrejOrsula/omtp_course -b master ./src/rob866_omtp_course
```

Install all other ROS dependencies
```bash
rosdep install --from-paths . --ignore-src --rosdistro ${ROS_DISTRO}
```

And finally build the packages of this repository with either `colcon` or `catkin`
```bash
# Colcon
colcon build --symlink-install
# Catkin
catkin build
```


## Usage
If not a part of `~/.bashrc`, make sure to source the global ROS installation.
```bash
source /opt/ros/melodic/setup.bash
```

Then source the ROS workspace overlay (if not done before).
```bash
# Colcon
source /path/to/awesome_ws/install/local_setup.bash
# Catkin
source /path/to/awesome_ws/devel/setup.bash
```

Now you can try out the individual assignments, see their respective documentation for more info.


## Authors
- Andrej Orsula
- Asger Printz Madsen

VS Code's [Live Share extension](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare-pack) was utilised during some of the development, where the specific commits contain a co-author.

## Acknowledgment
This repository contains several packages that were not developed by the authors of this project. The original authors of the ROS packages are listed under the corresponding `package.xml` manifests.


## License
This project is licensed under [BSD 3-Clause License](LICENSE).
