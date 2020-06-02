#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from omtp_factory_flexbe_states.set_conveyor_power_state import SetConveyorPowerState
from omtp_factory_flexbe_states.detect_part_camera_state import DetectPartCameraState
from flexbe_manipulation_states.moveit_to_joints_dyn_state import MoveitToJointsDynState as flexbe_manipulation_states__MoveitToJointsDynState
from omtp_factory_flexbe_states.compute_grasp_state import ComputeGraspState
from omtp_factory_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from omtp_factory_flexbe_states.control_feeder_state import ControlFeederState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 07 2020
@author: Andrej Orsula
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
		# x:1746 y:859, x:310 y:824
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.robot1_joint_names = robot1_joint_names
		_state_machine.userdata.robot1_home = robot1_home
		_state_machine.userdata.robot1_pregrasp = robot1_pregrasp
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.pick_configuration = []
		_state_machine.userdata.robot1_place = robot1_place
		_state_machine.userdata.computed_joint_names = []
		_state_machine.userdata.speed = 100.0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:52 y:25
			OperatableStateMachine.add('start_conveyor',
										SetConveyorPowerState(stop=False),
										transitions={'succeeded': 'start_feeder', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'speed': 'speed'})

			# x:697 y:72
			OperatableStateMachine.add('detect_part_on_conveyor',
										DetectPartCameraState(ref_frame='robot1_base_link', camera_topic='/omtp/logical_camera', camera_frame='logical_camera_frame'),
										transitions={'continue': 'move_pregrasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:1554 y:162
			OperatableStateMachine.add('move_grasp_approach',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'detect_part_on_conveyor_3', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:1670 y:467
			OperatableStateMachine.add('move_grasp',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'activate_gripper', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:1653 y:359
			OperatableStateMachine.add('compute_grasp',
										ComputeGraspState(group=robot1_move_group, offset=0.16, joint_names=robot1_joint_names, tool_link='vacuum_gripper1_suction_cup', rotation=3.1415),
										transitions={'continue': 'move_grasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:1681 y:581
			OperatableStateMachine.add('activate_gripper',
										VacuumGripperControlState(enable='true', service_name='/gripper1/control'),
										transitions={'continue': 'move_place', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1687 y:708
			OperatableStateMachine.add('move_place',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'robot1_place', 'joint_names': 'robot1_joint_names'})

			# x:498 y:58
			OperatableStateMachine.add('move_home',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'detect_part_on_conveyor', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'robot1_home', 'joint_names': 'robot1_joint_names'})

			# x:1332 y:123
			OperatableStateMachine.add('compute_grasp_approach',
										ComputeGraspState(group=robot1_move_group, offset=0.5, joint_names=robot1_joint_names, tool_link='vacuum_gripper1_suction_cup', rotation=3.1415),
										transitions={'continue': 'move_grasp_approach', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick_configuration', 'joint_names': 'computed_joint_names'})

			# x:283 y:40
			OperatableStateMachine.add('start_feeder',
										ControlFeederState(activation=True),
										transitions={'succeeded': 'move_home', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off})

			# x:904 y:88
			OperatableStateMachine.add('move_pregrasp',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=robot1_move_group, action_topic='/move_group'),
										transitions={'reached': 'detect_part_on_conveyor_2', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'robot1_pregrasp', 'joint_names': 'robot1_joint_names'})

			# x:1108 y:104
			OperatableStateMachine.add('detect_part_on_conveyor_2',
										DetectPartCameraState(ref_frame='robot1_base_link', camera_topic='/omtp/logical_camera', camera_frame='logical_camera_frame'),
										transitions={'continue': 'compute_grasp_approach', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:1627 y:260
			OperatableStateMachine.add('detect_part_on_conveyor_3',
										DetectPartCameraState(ref_frame='robot1_base_link', camera_topic='/omtp/logical_camera', camera_frame='logical_camera_frame'),
										transitions={'continue': 'compute_grasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
