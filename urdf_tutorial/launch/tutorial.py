"""Launch of a Gazebo instance with a model defined by xacro"""

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


    return LaunchDescription([


        # Start Gazebo instance
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory(
                'gazebo_ros'), 'launch', 'gazebo.launch.py'))
        ),

        # Spawn entity with corresponding urdf file
        Node(package='gazebo_ros',
             node_executable='spawn_entity.py',
             arguments=['-entity', 'OMTP', '-file', '../omtp_course/urdf_tutorial/urdf/05-visual.urdf'],
             output='screen'),
    ])
