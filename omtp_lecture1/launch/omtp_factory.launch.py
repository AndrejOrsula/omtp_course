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
    # Path to xacro defining Gazebo model
    xacro_path = os.path.join(get_package_share_directory(
        'omtp_lecture1'), 'urdf', 'omtp_factory_modified.xacro')

    # Convert xacro to urdf
    # Note: Using this ugly hack because xacro cannot be run as a ROS2 Node (explanation below)
    os.system('xacro %s -o /tmp/omtp.urdf' % xacro_path)

    return LaunchDescription([
        # Convert xacro to urdf
        # Note: Utilising xacro as a node does NOT currently work in eloquent.
        # Note: It complains about not supporting `--ros-args` argument (new in eloquent).
        # Node(
        #     package='xacro',
        #     node_executable='xacro',
        #     arguments=[
        #         [xacro_path,
        #          '-o',
        #          '/tmp/omtp.urdf']
        #     ],
        #     output='screen',
        # ),

        # Start Gazebo instance
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory(
                'gazebo_ros'), 'launch', 'gazebo.launch.py'))
        ),

        # Spawn entity with corresponding urdf file
        Node(package='gazebo_ros',
             node_executable='spawn_entity.py',
             arguments=['-entity', 'OMTP', '-file', '/tmp/omtp.urdf'],
             output='screen'),
    ])
