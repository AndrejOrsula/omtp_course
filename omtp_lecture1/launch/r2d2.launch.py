"""Launch of a Gazebo instance with a model defined by URDF"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir


def generate_launch_description():
    # Path to URDF defining Gazebo model
    urdf_path = os.path.join(get_package_share_directory(
        'urdf_tutorial'), 'urdf', 'r2r2.urdf')

    return LaunchDescription([
        # Start Gazebo instance
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory(
                'gazebo_ros'), 'launch', 'gazebo.launch.py'))
        ),

        # Spawn entity with corresponding urdf file
        # Path needs to be static otherwise `spawn_entity.py` return an error about not recognizing `--ros-args`
        Node(package='gazebo_ros',
             node_executable='spawn_entity.py',
             arguments=['-entity', 'r2d2', '-file', '/TODO/path/to/urdf_tutorial/urdf/r2d2.urdf'],
             output='screen'),
    ])
