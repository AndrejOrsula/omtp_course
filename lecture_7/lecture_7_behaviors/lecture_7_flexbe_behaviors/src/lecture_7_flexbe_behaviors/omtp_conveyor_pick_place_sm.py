#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_manipulation_states.moveit_to_joints_dyn_state import MoveitToJointsDynState as flexbe_manipulation_states__MoveitToJointsDynState
from omtp_factory_flexbe_states.detect_part_camera_state import DetectPartCameraState
from omtp_factory_flexbe_states.compute_grasp_state import ComputeGraspState
from omtp_factory_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 07 2020
@author: Andrej Orsula and Asger P. Madsen
'''
class omtp_conveyor_pick_placeSM(Behavior):
	'''
	Pick a part from conveyor and place in a bin
	'''


	def __init__(self):
		super(omtp_conveyor_pick_placeSM, self).__init__()
		self.name = 'omtp_conveyor_pick_place'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		robot1_move_group = 'robot1'
		robot1_joint_names = ['robot1_elbow_joint', 'robot1_shoulder_lift_joint', 'robot1_shoulder_pan_joint', 'robot1_wrist_1_joint', 'robot1_wrist_2_joint', 'robot1_wrist_3_joint']
		robot1_home = [1.5708, -1.5708, 1.5708, -1.5708, -1.5708, 0]
		robot1_pregrasp = [1.5708, -1.5708, 0.785398, -1.5708, -1.5708, 0]
		robot1_place = [1.5708, -1.5708, -1.5708, -1.5708, -1.5708, 0]
		# x:1453 y:843, x:25 y:857
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.robot1_joint_names = robot1_joint_names
		_state_machine.userdata.robot1_home = robot1_home
		_state_machine.userdata.robot1_pregrasp = robot1_pregrasp
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.pick_configuration = []
		_state_machine.userdata.robot1_place = robot1_place
		_state_machine.userdata.computed_joint_names = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:41 y:30
			OperatableStateMachine.add('move_home',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'detect_part_on_conveyor', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'robot1_home', 'joint_names': 'robot1_joint_names'})

			# x:246 y:53
			OperatableStateMachine.add('detect_part_on_conveyor',
										DetectPartCameraState(ref_frame='robot1_base_link', camera_topic='/omtp/logical_camera', camera_frame='logical_camera_frame'),
										transitions={'continue': 'compute_pregrasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:442 y:71
			OperatableStateMachine.add('compute_pregrasp',
										ComputeGraspState(group=robot1_move_group, offset=0.175, joint_names=robot1_joint_names, tool_link='vacuum_gripper1_suction_cup', rotation=3.1415),
										transitions={'continue': 'move_pregrasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:640 y:118
			OperatableStateMachine.add('move_pregrasp',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'compute_grasp', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:1084 y:209
			OperatableStateMachine.add('move_grasp',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'activate_gripper', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:854 y:160
			OperatableStateMachine.add('compute_grasp',
										ComputeGraspState(group=robot1_move_group, offset=0.15, joint_names=robot1_joint_names, tool_link='vacuum_gripper1_suction_cup', rotation=3.1415),
										transitions={'continue': 'move_grasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:1308 y:264
			OperatableStateMachine.add('activate_gripper',
										VacuumGripperControlState(enable='true', service_name='/gripper1/control'),
										transitions={'continue': 'move_place', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1319 y:377
			OperatableStateMachine.add('move_place',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'activate_gripper_2', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'robot1_place', 'joint_names': 'robot1_joint_names'})

			# x:1314 y:485
			OperatableStateMachine.add('activate_gripper_2',
										VacuumGripperControlState(enable='false', service_name='/gripper1/control'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
