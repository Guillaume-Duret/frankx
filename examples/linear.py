from argparse import ArgumentParser

from frankx import Affine, LinearRelativeMotion, Robot
from frankx import *


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', default='172.168.0.2', help='FCI IP of the robot')
    parser.add_argument('--d_grasp', default='0.12', help='Approch distance from the current position')
    parser.add_argument('--force', default='1.0', help='force used to graping')

    args = parser.parse_args()

    d_grasp = -float(args.d_grasp)
    force_used = float(args.force)
    print(force_used)

    # Connect to the robot
    robot = Robot(args.host)
    robot.set_default_behavior()
    robot.recover_from_errors()
    gripper = robot.get_gripper()
    gripper.gripper_speed = 0.05 #  [m/s]
    gripper.gripper_force = force_used #  [N]
    gripper.move(gripper.max_width)
    print(gripper.max_width)

    # Reduce the acceleration and velocity dynamic
    robot.set_dynamic_rel(0.04)

    joint_motion = JointMotion([-0.3183561079422883, 0.17575251615674872, 0.2996618963417813, -2.35075751401161, -0.08695447695993458, 2.514809009284535, 0.8327488414463068])
    robot.move(joint_motion)



    # 
    #gripper.move(50.0) # [mm]


    # Define and move forwards way = Affine(-0.008086, -0.002156, 0,1)
    way = Affine(0.0, 0.0, d_grasp)
    motion_forward = LinearRelativeMotion(way)
    robot.move(motion_forward)


    gripper.clamp()
    #gripper.move(50.0)

    

    # And move backwards using the inverse motion
    motion_backward = LinearRelativeMotion(way.inverse())
    robot.move(motion_backward)


    motion_forward = LinearRelativeMotion(way)
    robot.move(motion_forward)
    gripper.move(gripper.max_width)

    # And move backwards using the inverse motion
    motion_backward = LinearRelativeMotion(way.inverse())
    robot.move(motion_backward)
