import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray

class HeadTiltClient(Node):

    def __init__(self):
        super().__init__('head_tilt_client')
        # Action client to send goals to jaw controller
        self.eye_action_client_horizontal = ActionClient(self, FollowJointTrajectory, '/head_controller/follow_joint_trajectory')
        # Subscriber to get data from face tracker
        self.get_data = self.create_subscription(
            Float32MultiArray,
            'tilt_head',
            self.send_goal,
            10,
        )

    def send_goal(self, position):
        # Message type in JointTrajectory
        goal_msg = JointTrajectory()

        # Joint trajectory points
        jtp = JointTrajectoryPoint()
        jtp.velocities = [0.0]
        jtp.time_from_start.sec = 0
        jtp.time_from_start.nanosec = 0   
        jtp.positions = [position.data[0]]

        if position.data[1] == 1.0:
            joint = "head_tilt_right_joint"
        elif position.data[1] == 0.0:
            joint = "head_tilt_vertical_joint"
        elif position.data[1] == -1.0:
            joint = "head_tilt_left_joint"

        jointNames = []
        jointNames.append(joint)

        # Build message
        goal_msg.points = [jtp]
        goal_msg.joint_names = jointNames

        # Assign goal
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = goal_msg

        self.eye_action_client_horizontal.wait_for_server()

        self.get_logger().info('Goal: %f' % jtp.positions[0])

        self.eye_action_client_horizontal.send_goal_async(goal)


def main(args=None):

    rclpy.init(args=args)

    head_tilt_client = HeadTiltClient()

    rclpy.spin(head_tilt_client)

    head_tilt_client.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
