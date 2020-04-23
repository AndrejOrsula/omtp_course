# ROB866 - OMTP
![OS](https://img.shields.io/badge/OS-Ubuntu_18.04-orange.svg) ![ROS_2](https://img.shields.io/badge/ROS_2-Eloquent-brightgreen.svg) ![GAZEBO](https://img.shields.io/badge/Gazebo-9.12-lightgrey.svg)

**Note: This branch is discontinued due to missing MoveIt 2 functionalities that are not yet migrated as of April 2020, see [MoveIt 2 Migration Progress](https://docs.google.com/spreadsheets/d/1aPb3hNP213iPHQIYgcnCYh9cGFUlZmi_06E_9iTSsOI/edit?usp=sharing).**

This repository contains assignment of group ROB866 for *Object Manipulation and Task Planning (Robotics 8)* course at *Aalborg University*, *Denmark*.

## Description
The repository itself contains assignments for the lectures/exercises structured as the following packages.
- [`omtp_lecture1`](omtp_lecture1/)

Furthermore, several packages that provide *URDF* models, some in form of *xacro*, are also included so that these can be spawned in Gazebo. All of these packages were ported to ROS 2.
- [`urdf_tutorial`](urdf_tutorial/)
- [`omtp_support`](omtp_support/)
- [`ur_description`](ur_description/)
- [`abb_irb6640_support`](abb_irb6640_support/)
- [`kinova_description`](kinova_description/)


### ROS 2 Differences
As this repository utilises ROS 2 Eloquent instead of a ROS 1 distribution, solving of the assignments has some differences. These are further documented [here](ros2_differences.md).



## Installation
The following installation instructions were tested with OS based on *Ubuntu 18.04 LTS (Bionic Beaver)*.

### Requirements

#### 1) [ROS 2 Eloquent](https://index.ros.org/doc/ros2/Installation/Eloquent) with [Development Tools](https://index.ros.org/doc/ros2/Installation/Eloquent/Linux-Development-Setup/#install-development-tools-and-ros-tools)
Feel free to follow the instructions or use the provided [installation script](scripts/install_ros2_distro_eloquent.bash).

#### 2) [Gazebo](http://gazebosim.org/tutorials?tut=install_ubuntu&cat=install) (tested with 9.12)
```bash
curl -sSL http://get.gazebosim.org | sh
```

#### 3) [Xacro (XML Macros)](https://github.com/ros/xacro/tree/dashing-devel)
```bash
sudo apt-get install -y ros-eloquent-xacro
```

### Building
```bash
git clone https://github.com/AndrejOrsula/omtp_course -b ros2 && cd omtp_course
source /opt/ros/eloquent/setup.bash
colcon build --symlink-install
```


## Usage
First, source the ROS 2 global installation (if not done before).
```bash
source /opt/ros/eloquent/setup.bash
```

Then source the ROS 2 workspace overlay (if not done before).
```bash
source /path/to/omtp_course/install/local_setup.bash
```

Now you can run the assignments with the following launch scripts.
```bash
ros2 launch omtp_lecture1 omtp_factory.launch.py
ros2 launch omtp_lecture1 r2d2.launch.py # This script requires path to be manually edited (eloquent bug)
```


## Authors
- Andrej Orsula
- Asger Printz Madsen


## Acknowledgment
This repository contains several packages that were not developed by the authors of this project. The original authors of the ROS packages, which were ported to ROS 2, are listed under the corresponding `package.xml` manifests.


## License
This project is licensed under [BSD 3-Clause License](LICENSE).
