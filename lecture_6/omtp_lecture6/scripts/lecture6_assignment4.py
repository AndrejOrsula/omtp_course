#!/usr/bin/env python

import rospy
import tf2_ros
import tf2_geometry_msgs
import geometry_msgs
import moveit_commander
import sys

from omtp_gazebo.msg import LogicalCameraImage
from omtp_gazebo.srv import VacuumGripperControl
from std_srvs.srv import Empty


def lecture6_assignment4():
    """Perform pick and place task"""
    # Setup this ROS node
    rospy.init_node('lecture6_assignment4', anonymous=True)

    # Setup MoveIt
    moveit_commander.roscpp_initialize(sys.argv)
    robot2_group = moveit_commander.MoveGroupCommander("robot2")

    # Setup client for the gripper
    rospy.wait_for_service('/gripper2/control')
    gripper = rospy.ServiceProxy('/gripper2/control', VacuumGripperControl)
    gripper(False)

    # Setup tf2 listener
    global tf_buffer
    tf_buffer = tf2_ros.Buffer()
    tf2_ros.TransformListener(tf_buffer)

    # Setup object spawner
    rospy.wait_for_service('/start_spawn')
    start_spawn = rospy.ServiceProxy('/start_spawn', Empty)
    rospy.wait_for_service('/stop_spawn')
    stop_spawn = rospy.ServiceProxy('/stop_spawn', Empty)

    # Spawn the first object
    start_spawn()
    rospy.sleep(1.95)
    stop_spawn()

    # Move home
    robot2_group.set_named_target("R2Home")
    robot2_group.go(wait=True)

    while not rospy.is_shutdown():
        # Get pose of the object in world coordinate frame
        is_object_found, object_pose_wrt_world = get_object_pose()

        # Make sure the object is spawned and camera can see it
        if not is_object_found:
            rospy.sleep(2.0)
            continue

        # Get current robot pose
        current_robot2_pose = robot2_group.get_current_pose()

        # Create grasp pose from the object pose
        grasp_pose = object_pose_wrt_world.pose
        grasp_pose.position.z = grasp_pose.position.z + 0.145
        grasp_pose.orientation = current_robot2_pose.pose.orientation

        # Move to grasp pose
        robot2_group.set_pose_target(grasp_pose)
        successful = robot2_group.go(wait=True)

        # Try again if planning was not successful
        if not successful:
            continue

        # If succesful, grasp the object
        gripper(True)

        # Move home and then placing pose
        robot2_group.set_named_target("R2Home")
        robot2_group.go(wait=True)
        robot2_group.set_named_target("R2Place")
        robot2_group.go(wait=True)

        # Release the grasped object
        gripper(False)

        # Spawn another object
        # This does not always work when CPU is under load - spawn with CLI if it fails
        start_spawn()
        rospy.sleep(1.95)
        stop_spawn()

        # Go back home
        robot2_group.set_named_target("R2PreGrasp")
        robot2_group.go(wait=True)

    # When finished shut down moveit commander
    moveit_commander.roscpp_shutdown()


def get_object_pose():
    """Get object pose wrt. world"""
    is_object_found = False
    object_pose_wrt_world = geometry_msgs.msg.PoseStamped()

    # Wait for message from logical camera
    data = rospy.wait_for_message('/omtp/logical_camera_2', LogicalCameraImage)

    # Find the specific object
    for model in data.models:
        if (model.type == 'object'):

            # Convert to stamped msg
            object_pose_wrt_camera = geometry_msgs.msg.PoseStamped()
            object_pose_wrt_camera.header.stamp = rospy.Time.now()
            object_pose_wrt_camera.header.frame_id = "logical_camera_2_frame"
            object_pose_wrt_camera.pose = model.pose

            # Transform to world coordinate frame
            while True:
                try:
                    global tf_buffer
                    object_pose_wrt_world = tf_buffer.transform(
                        object_pose_wrt_camera, "world")
                    break
                except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                    continue
            is_object_found = True
            break

    return is_object_found, object_pose_wrt_world


if __name__ == '__main__':
    """Start the node"""
    try:
        lecture6_assignment4()
    except rospy.ROSInterruptException:
        pass
